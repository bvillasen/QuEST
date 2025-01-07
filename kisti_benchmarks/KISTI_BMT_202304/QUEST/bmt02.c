/** @file 
 *  KISTI-6 QC-BMT Prob02 
 *  
 *  @author Hoon Ryu
 */

#include <stdio.h>
#include "QuEST.h"
#include <mpi.h>
#include <math.h>

int main (int narg, char *varg[]) {
    
	int ii = 0, jj = 0;
	int Nqubit = 19;
	int Cdim = 2*Nqubit + 1;
	double elapsed_time01 = 0, elapsed_time02 = 0, elapsed_time03 = 0;
	QuESTEnv env = createQuESTEnv();

    	if(env.rank == 0)
    	{   
        	printf("-------------------------------------------------------------------------------\n");
        	printf("Running BMT:\n\tHadamard-test circuit: Getting expectation of a certain unitary\n");
        	printf("-------------------------------------------------------------------------------\n");
    	}

	elapsed_time01 = -MPI_Wtime();
	
	Qureg qubits = createQureg(Cdim, env);
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

	for(ii = 0; ii < Cdim; ii++)
		hadamard(qubits, ii);

	for(ii = Nqubit+1; ii <= 2*Nqubit; ii++)
	{
		for(jj = 1; jj <= Nqubit; jj++)
		{			
			controlledNot(qubits, jj, ii);
			controlledRotateZ(qubits, 0, ii, 3.14159265358979323846/4.0);
			controlledNot(qubits, jj, ii);
		}
	}
	
	hadamard(qubits, 0);

	elapsed_time02 += MPI_Wtime();
    
    	if(env.rank == 0)
    	{
        	printf("\n");
        	printf("----------------------------------\n");
        	printf("Printing Amplitudes & Finishing...\n");
        	printf("----------------------------------\n");
    	}

	elapsed_time03 = -MPI_Wtime();

	qreal prob0 = 0, prob1 = 0;
	prob0 = calcProbOfOutcome(qubits, 0, 0);
	prob1 = calcProbOfOutcome(qubits, 0, 1);
	
	if(env.rank == 0)
	{
		printf("Probability of qubit 0 being in state 0: %g\n", prob0);
		printf("Probability of qubit 0 being in state 1: %g\n", prob1);
	}

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

    	destroyQuESTEnv(env);

    	return 0;
}
