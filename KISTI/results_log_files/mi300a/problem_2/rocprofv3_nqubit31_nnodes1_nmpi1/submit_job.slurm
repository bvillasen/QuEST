#!/bin/bash

echo "Starting job. $(date)"


# Set the QuEST environment
export QUEST_ROOT=/home/bvillase/code/kisti/QuEST
SYSTEM=pp_conductor source /home/bvillase/code/kisti/QuEST/scripts/set_env.sh

# Call application run script
echo "Starting app run. $(date)"
BENCHMARK_PROB=2 N_QUBIT=15 N_MPI=1 WORK_DIR=/home/bvillase/benchmarks/quest/problem_2/rocprofv3_nqubit31_nnodes1_nmpi1 PROFILER=rocprofv3_stats bash /home/bvillase/code/kisti/QuEST/scripts/run_app.sh
echo "Finished app run. $(date)"


echo "Finished job. $(date)"
