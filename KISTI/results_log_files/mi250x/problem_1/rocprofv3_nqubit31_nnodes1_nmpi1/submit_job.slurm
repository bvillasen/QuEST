#!/bin/bash

#SBATCH -J Q1_n31
#SBATCH --time=0:00:00
#SBATCH --no-requeue
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=8
#SBATCH --threads-per-core=1
#SBATCH -D /home/bvillase/benchmarks/quest/mi250x/problem_1/rocprofv3_nqubit31_nnodes1_nmpi1
#SBATCH -e /home/bvillase/benchmarks/quest/mi250x/problem_1/rocprofv3_nqubit31_nnodes1_nmpi1/job_error.log
#SBATCH -o /home/bvillase/benchmarks/quest/mi250x/problem_1/rocprofv3_nqubit31_nnodes1_nmpi1/job_output.log
#SBATCH --exclusive


echo "SLUM_NODES=$SLURM_NNODES  NODE_LIST:$SLURM_NODELIST"
echo "Starting SLURM job. $(date)"


# Set the QuEST environment
export QUEST_ROOT=/home/bvillase/code/kisti/QuEST
SYSTEM=lockhart_mi250x source /home/bvillase/code/kisti/QuEST/scripts/set_env.sh

# Call application run script
echo "Starting app run. $(date)"
BENCHMARK_PROB=1 N_QUBIT=31 N_MPI=1 WORK_DIR=/home/bvillase/benchmarks/quest/mi250x/problem_1/rocprofv3_nqubit31_nnodes1_nmpi1 PROFILER=rocprofv3_stats bash /home/bvillase/code/kisti/QuEST/scripts/run_app.sh
echo "Finished app run. $(date)"


echo "Finished SLURM job. $(date)"
