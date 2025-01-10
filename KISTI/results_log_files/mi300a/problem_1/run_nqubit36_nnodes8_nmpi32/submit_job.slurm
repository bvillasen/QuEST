#!/bin/bash
#SBATCH -p MI300
#SBATCH -J Q1_n36
#SBATCH --time=0:00:00
#SBATCH --no-requeue
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=4
#SBATCH --threads-per-core=1
#SBATCH -D /home/bvillase/benchmarks/quest/mi300a/problem_1/run_nqubit36_nnodes8_nmpi32
#SBATCH -e /home/bvillase/benchmarks/quest/mi300a/problem_1/run_nqubit36_nnodes8_nmpi32/job_error.log
#SBATCH -o /home/bvillase/benchmarks/quest/mi300a/problem_1/run_nqubit36_nnodes8_nmpi32/job_output.log
#SBATCH --exclusive
#SBATCH --exclude x1001c0s1b0n0 


echo "SLUM_NODES=$SLURM_NNODES  NODE_LIST:$SLURM_NODELIST"
echo "Starting SLURM job. $(date)"


# Set the QuEST environment
export QUEST_ROOT=/home/bvillase/code/kisti/QuEST
SYSTEM=lockhart_mi300a source /home/bvillase/code/kisti/QuEST/scripts/set_env.sh

# Call application run script
echo "Starting app run. $(date)"
BENCHMARK_PROB=1 N_QUBIT=36 N_MPI=32 WORK_DIR=/home/bvillase/benchmarks/quest/mi300a/problem_1/run_nqubit36_nnodes8_nmpi32 PROFILER= bash /home/bvillase/code/kisti/QuEST/scripts/run_app.sh
echo "Finished app run. $(date)"


echo "Finished SLURM job. $(date)"
