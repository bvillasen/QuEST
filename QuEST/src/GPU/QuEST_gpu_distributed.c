/** @file
 * Implementation of distributed version of some of the GPU functions for the KISTI RFP.
 *
 * @author Bruno Villasenor (AMD) bruno.villasenoralvarez@amd.com
 */

# include "QuEST.h"
# include "QuEST_precision.h"
# include "QuEST_validation.h"

# include <stdlib.h>
# include <stdio.h>
# include <mpi.h>

// Distributed version of the createQuESTEnv for multiple GPUs
QuESTEnv createQuESTEnvDistributed(void){
    
    QuESTEnv env;

    // printf("Initializing MPI \n");
    // init MPI environment
    int rank, numRanks, initialized;
    MPI_Initialized(&initialized);
    if (!initialized){
        MPI_Init(NULL, NULL);
        MPI_Comm_size(MPI_COMM_WORLD, &numRanks);
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);

        env.rank=rank;
        env.numRanks=numRanks;

    } else {
        
        printf("ERROR: Trying to initialize QuESTEnv multiple times. Ignoring...\n");
        
        // ensure env is initialised anyway, so the compiler is happy
        MPI_Comm_size(MPI_COMM_WORLD, &numRanks);
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        env.rank=rank;
        env.numRanks=numRanks;
	}
    
    validateNumRanks(env.numRanks, __func__);
    
    env.seeds = NULL;
    env.numSeeds = 0;
    seedQuESTDefault(&env);

    // Get the in-node rank wich will be used to se the device number
    MPI_Comm shmcomm;
    MPI_Comm_split_type(MPI_COMM_WORLD, MPI_COMM_TYPE_SHARED, 0,
                        MPI_INFO_NULL, &shmcomm);
    int shmrank;
    MPI_Comm_rank(shmcomm, &shmrank);
    env.inNodeRank = shmrank;

    return env;
}

void synchronizeMPI(void){
    MPI_Barrier(MPI_COMM_WORLD);
}

void finalizeMPI(void){
    int finalized;
    MPI_Finalized(&finalized);
    if (!finalized) MPI_Finalize();
    else printf("ERROR: Trying to close QuESTEnv multiple times. Ignoring\n");
}


void exchangeDeviceStateVectors(Qureg qureg, int pairRank){
    // MPI send/receive vars
    int TAG=100;
    // MPI_Status status;

    // Multiple messages are required as MPI uses int rather than long long int for count
    // For openmpi, messages are further restricted to 2GB in size -- do this for all cases
    // to be safe
    long long int maxMessageCount = MPI_MAX_AMPS_IN_MSG;
    // long long int maxMessageCount = qureg.numAmpsPerChunk;
    if (qureg.numAmpsPerChunk < maxMessageCount) 
        maxMessageCount = qureg.numAmpsPerChunk;
    
    // safely assume MPI_MAX... = 2^n, so division always exact
    int numMessages = qureg.numAmpsPerChunk/maxMessageCount;
    int i;
    long long int offset;

    // Wait for the device before the transfers
    deviceSynchronize();

    #ifdef TIMERS
    *(qureg.mpi_time) -= MPI_Wtime();
    int mpi_type_size;
    MPI_Type_size(MPI_QuEST_REAL, &mpi_type_size);
    *(qureg.mpi_total_transfer_size) += 2 * numMessages * maxMessageCount *  mpi_type_size; 
    #endif

    #ifdef PRINT_MPI_IDS
    printf( "Exchange rank: %d   pairRank: %d   numMessages: %d   maxMessageCount %lld\n", qureg.chunkId, pairRank, numMessages, maxMessageCount );
    #endif

    int num_requests = 2*numMessages;

    #ifdef GPU_MPI
    MPI_Request send_reqs[num_requests];
    MPI_Request recv_reqs[num_requests];
    #endif

    // send my state vector to pairRank's qureg.pairStateVec
    // receive pairRank's state vector into qureg.pairStateVec
    for (i=0; i<numMessages; i++){
        offset = i*maxMessageCount;
        #ifdef GPU_MPI
        // Transfer the GPU arrays directly
        // MPI_Sendrecv(&qureg.deviceStateVec.real[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG,
        //         &qureg.devicePairStateVec.real[offset], maxMessageCount, MPI_QuEST_REAL,
        //         pairRank, TAG, MPI_COMM_WORLD, &status);
        // //printf("rank: %d err: %d\n", qureg.rank, err);
        // MPI_Sendrecv(&qureg.deviceStateVec.imag[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG,
        //         &qureg.devicePairStateVec.imag[offset], maxMessageCount, MPI_QuEST_REAL,
        //         pairRank, TAG, MPI_COMM_WORLD, &status);

        // Non-blocking implementation
        MPI_Isend(&qureg.deviceStateVec.real[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG, MPI_COMM_WORLD, &send_reqs[i] );
        MPI_Isend(&qureg.deviceStateVec.imag[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG, MPI_COMM_WORLD, &send_reqs[numMessages+i] );
        MPI_Irecv(&qureg.devicePairStateVec.real[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG, MPI_COMM_WORLD, &recv_reqs[i] );
        MPI_Irecv(&qureg.devicePairStateVec.imag[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG, MPI_COMM_WORLD, &recv_reqs[numMessages + i] );


        #else
        
        // Copy arrays from GPU to Host before
        copyStateFromGPU(qureg);

        // Transfer the Host arrays
        MPI_Sendrecv(&qureg.stateVec.real[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG,
                &qureg.pairStateVec.real[offset], maxMessageCount, MPI_QuEST_REAL,
                pairRank, TAG, MPI_COMM_WORLD, &status);
        //printf("rank: %d err: %d\n", qureg.rank, err);
        MPI_Sendrecv(&qureg.stateVec.imag[offset], maxMessageCount, MPI_QuEST_REAL, pairRank, TAG,
                &qureg.pairStateVec.imag[offset], maxMessageCount, MPI_QuEST_REAL,
                pairRank, TAG, MPI_COMM_WORLD, &status);

        // Copy arrays from Host to GPU after the transfer
        copyPairStateToGPU(qureg);
        #endif
    }

    #ifdef GPU_MPI    
    // Wait for all send and receive requests to finish
    MPI_Waitall( num_requests, &send_reqs[0], MPI_STATUSES_IGNORE );
    MPI_Waitall( num_requests, &recv_reqs[0], MPI_STATUSES_IGNORE );
    #endif
    
    #ifdef TIMERS
    *(qureg.mpi_time) += MPI_Wtime();
    #endif
}

static int getChunkIdFromIndex(Qureg qureg, long long int index);
// Copied from QuEST_cpu_distributed.c
int getChunkIdFromIndex(Qureg qureg, long long int index){
    return index/qureg.numAmpsPerChunk; // this is numAmpsPerChunk
}

qreal statevec_getRealAmpDistributed(Qureg qureg, long long int index){
    
    int chunkId = getChunkIdFromIndex(qureg, index);
    qreal el; 
    if (qureg.chunkId==chunkId){
        copy_qrealFromGPU( &el, &(qureg.deviceStateVec.real[index-chunkId*qureg.numAmpsPerChunk]), sizeof(*(qureg.deviceStateVec.real)) );
        deviceSynchronize();
    }
    MPI_Bcast(&el, 1, MPI_QuEST_REAL, chunkId, MPI_COMM_WORLD);
    return el;
}

qreal statevec_getImagAmpDistributed(Qureg qureg, long long int index){
    
    int chunkId = getChunkIdFromIndex(qureg, index);
    qreal el; 
    if (qureg.chunkId==chunkId){
        copy_qrealFromGPU( &el, &(qureg.deviceStateVec.imag[index-chunkId*qureg.numAmpsPerChunk]), sizeof(*(qureg.deviceStateVec.imag)) );
        deviceSynchronize();
    }
    MPI_Bcast(&el, 1, MPI_QuEST_REAL, chunkId, MPI_COMM_WORLD);
    return el;
}

qreal reduceStateProb( Qureg qureg, qreal stateProb ){
    qreal totalStateProb = 0;
    MPI_Allreduce(&stateProb, &totalStateProb, 1, MPI_QuEST_REAL, MPI_SUM, MPI_COMM_WORLD);
    return totalStateProb;
}

void print_global_metric_statistics(qreal local_metric, QuESTEnv env){
    double v_min, v_max, v_sum, v_avg;
    MPI_Reduce(&local_metric,  &v_min, 1, MPI_DOUBLE, MPI_MIN, 0, MPI_COMM_WORLD );
    MPI_Reduce(&local_metric,  &v_max, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD );
    MPI_Reduce(&local_metric,  &v_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD );
    v_avg = v_sum / env.numRanks;

    char buffer[100];
    sprintf( buffer, "min: %.2f   max: %.2f  avrg: %.2f ", v_min, v_max, v_avg );

    if(env.rank == 0) printf( "%s", buffer) ;
}