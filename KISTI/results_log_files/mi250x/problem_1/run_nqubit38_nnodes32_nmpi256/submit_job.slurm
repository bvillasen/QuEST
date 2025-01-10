#!/bin/bash

#SBATCH -J Q1_n38
#SBATCH --time=0:00:00
#SBATCH --no-requeue
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=8
#SBATCH --gpus-per-node=8
#SBATCH --threads-per-core=1
#SBATCH -D /home/bvillase/benchmarks/quest/mi250x/problem_1/run_nqubit38_nnodes32_nmpi256
#SBATCH -e /home/bvillase/benchmarks/quest/mi250x/problem_1/run_nqubit38_nnodes32_nmpi256/job_error.log
#SBATCH -o /home/bvillase/benchmarks/quest/mi250x/problem_1/run_nqubit38_nnodes32_nmpi256/job_output.log
#SBATCH --exclusive
#SBATCH --exclude x1000c1s4b0n0,x1000c4s2b0n0,x1000c2s4b1n0,x1000c5s4b1n0 


echo "SLUM_NODES=$SLURM_NNODES  NODE_LIST:$SLURM_NODELIST"
echo "Starting SLURM job. $(date)"


# Set the QuEST environment
export QUEST_ROOT=/home/bvillase/code/kisti/QuEST
SYSTEM=lockhart_mi250x source /home/bvillase/code/kisti/QuEST/scripts/set_env.sh

# Call application run script
echo "Starting app run. $(date)"
BENCHMARK_PROB=1 N_QUBIT=38 N_MPI=256 WORK_DIR=/home/bvillase/benchmarks/quest/mi250x/problem_1/run_nqubit38_nnodes32_nmpi256 bash ${QUEST_ROOT}/scripts/run_app.sh
echo "Finished app run. $(date)"


echo "Finished SLURM job. $(date)"
