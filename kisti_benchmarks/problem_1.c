/** @file 
 * KISTI-6 QC-BMT Prob01 
 *
 * @author Hoon Ryu
 */

#include <stdio.h>
#include <mpi.h>
#include "QuEST.h"
#include <stdlib.h>

int main (int narg, char *varg[]) {

    	int Nqubit = 40;
			if (narg > 1){
				Nqubit = atoi(varg[1]);
			}
			
			int index = 0, index1 = 0;
    	double elapsed_time01 = 0, elapsed_time02 = 0, elapsed_time03 = 0;
    	QuESTEnv env = createQuESTEnv();

    	if(env.rank == 0)
    	{
    		printf("---------------------------------------------------------------------------------\n");
    		printf("Running BMT:\n\tBasic circuit involving a sequential conduction of X & CNOT gates\n");
    		printf("---------------------------------------------------------------------------------\n");
    	}

    	elapsed_time01 = -MPI_Wtime();

    	Qureg qubits = createQureg(Nqubit, env);
    	initZeroState(qubits);

    	elapsed_time01 += MPI_Wtime();

    	if(env.rank == 0)
    	{   
		printf("\n");
		printf("-------------------\n");
    		printf("Basic Configuration\n");
		printf("-------------------\n");
    	}
    	reportQuregParams(qubits);
    	reportQuESTEnv(env);

    	if(env.rank == 0)
    	{
     		printf("\n");
		printf("------------------\n");
		printf("Running Circuit...\n");
		printf("------------------\n");
    	}

    	elapsed_time02 = -MPI_Wtime();
    
	qreal prob; 
    	pauliX(qubits, 0);

    	for(index1 = 0; index1 < 30; index1++)
    	{
		if(env.rank == 0)
   			printf("loop = %d\n", index1+1);

    		for(index = 0; index < Nqubit-1; index++)
    	   		controlledNot(qubits, index, index+1);
        
		prob = getProbAmp(qubits, qubits.numAmpsTotal-1);
		if(env.rank == 0)
			printf("Probability amplitude of |1...1>: %g\n", prob);

   		for(index = 1; index < Nqubit; index++)
	    		pauliX(qubits, index);
        
		prob = getProbAmp(qubits, qubits.numAmpsTotal-1);
		if(env.rank == 0)
			printf("Probability amplitude of |1...1>: %g\n", prob);
    	}

			// Bruno V: Synchronize the device before the timer
			syncQuESTEnv( env );

    	elapsed_time02 += MPI_Wtime();

    	if(env.rank == 0)
    	{   
        	printf("\n");
        	printf("------------\n");
        	printf("Finishing...\n");
        	printf("------------\n");
    	}

    	elapsed_time03 = -MPI_Wtime();

			#ifdef TIMERS
			double mpi_time = *(qubits.mpi_time);
			double mpi_total_transfer_size = *(qubits.mpi_total_transfer_size) / 1024 / 1024 / 1024; //Convert to GB
			#endif

    	destroyQureg(qubits, env); 

    	elapsed_time03 += MPI_Wtime();

	MPI_Barrier(MPI_COMM_WORLD);

    	if(env.rank == 0)
    	{
		printf("\n");
		printf("Time components:\n");
		printf("---------------------------------------------------\n");
		printf("Allocation & Initialization: %e (seconds)\n", elapsed_time01);
		printf("Circuit Operation:           %e (seconds)\n", elapsed_time02);
		printf("Deallocation:                %e (seconds)\n", elapsed_time03);
		printf("---------------------------------------------------\n"); 
    	}

			#ifdef TIMERS
			if (env.rank ==0) printf( "MPI time. ");
			print_global_metric_statistics(mpi_time, env);
			if (env.rank ==0) printf( "secs \n");
			
			if (env.rank ==0) printf( "MPI transfer size. ");
			print_global_metric_statistics(mpi_total_transfer_size, env);
			if (env.rank ==0) printf( "GB \n");

			if (env.rank ==0) printf( "MPI Bandwidth per rank. ");
			print_global_metric_statistics(mpi_total_transfer_size/mpi_time, env);
			if (env.rank ==0) printf( "GB/s \n");

			#endif

    	destroyQuESTEnv(env);
    
    	return 0;
}
