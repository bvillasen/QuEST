#!/bin/bash

echo "Starting job. $(date)"


# Set the QuEST environment
export QUEST_ROOT=/home/bvillase/code/kisti/QuEST
SYSTEM=pp_conductor source /home/bvillase/code/kisti/QuEST/scripts/set_env.sh

# Call application run script
echo "Starting app run. $(date)"
BENCHMARK_PROB=1 N_QUBIT=33 N_MPI=4 WORK_DIR=/home/bvillase/benchmarks/quest/problem_1/run_nqubit33_nnodes1_nmpi4 PROFILER= bash /home/bvillase/code/kisti/QuEST/scripts/run_app.sh
echo "Finished app run. $(date)"


echo "Finished job. $(date)"
