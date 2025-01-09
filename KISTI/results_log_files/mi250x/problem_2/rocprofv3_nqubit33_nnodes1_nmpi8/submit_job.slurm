#!/bin/bash

#SBATCH -J Q2_n33
#SBATCH --time=0:00:00
#SBATCH --no-requeue
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gpus-per-node=8
#SBATCH --threads-per-core=1
#SBATCH -D /home/bvillase/benchmarks/quest/mi250x/problem_2/rocprofv3_nqubit33_nnodes1_nmpi8
#SBATCH -e /home/bvillase/benchmarks/quest/mi250x/problem_2/rocprofv3_nqubit33_nnodes1_nmpi8/job_error.log
#SBATCH -o /home/bvillase/benchmarks/quest/mi250x/problem_2/rocprofv3_nqubit33_nnodes1_nmpi8/job_output.log
#SBATCH --exclusive
#SBATCH --exclude x1000c1s7b0n0,x1000c3s3b0n0 


echo "SLUM_NODES=$SLURM_NNODES  NODE_LIST:$SLURM_NODELIST"
echo "Starting SLURM job. $(date)"


# Set the QuEST environment
export QUEST_ROOT=/home/bvillase/code/kisti/QuEST
SYSTEM=lockhart_mi250x source /home/bvillase/code/kisti/QuEST/scripts/set_env.sh

# Call application run script
echo "Starting app run. $(date)"
BENCHMARK_PROB=2 N_QUBIT=16 N_MPI=8 WORK_DIR=/home/bvillase/benchmarks/quest/mi250x/problem_2/rocprofv3_nqubit33_nnodes1_nmpi8 PROFILER=rocprofv3_stats bash /home/bvillase/code/kisti/QuEST/scripts/run_app.sh
echo "Finished app run. $(date)"


echo "Finished SLURM job. $(date)"
