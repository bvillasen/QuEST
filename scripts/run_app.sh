#!/bin/bash


if [[ -z "${QUEST_ROOT}" ]]; then
  echo -e "The QUEST_ROOT environment variable should be set"
  echo "Did you remember to `source scripts/set_env.sh` in the QuEST directory ?"
  return
fi


if [[ "${QUEST_SYSTEM}" == "lockhart_cpu" ]]; then
  QUEST_EXEC=${QUEST_ROOT}/build/quest_problem_${BENCHMARK_PROB}_cpu
  AFFINITY="-c 1"
  SRUN="srun"
elif [[ "${QUEST_SYSTEM}" == "lockhart_mi250x" ]]; then
  QUEST_EXEC=${QUEST_ROOT}/build_mi250x/quest_problem_${BENCHMARK_PROB}
  AFFINITY="--cpu-bind=verbose --cpu-bind=mask_cpu:ff000000000000,ff00000000000000,ff0000,ff000000,ff,ff00,ff00000000,ff0000000000"
  SRUN="srun"
elif [[ "${QUEST_SYSTEM}" == "lockhart_mi300a" ]]; then
  QUEST_EXEC=${QUEST_ROOT}/build_mi300a/quest_problem_${BENCHMARK_PROB}
  AFFINITY=${QUEST_ROOT}/scripts/slurm_affinity_mi300a.sh
  SRUN="srun"
elif [[ "${QUEST_SYSTEM}" == "pp_conductor" ]]; then
  QUEST_EXEC=${QUEST_ROOT}/build_mi300a/quest_problem_${BENCHMARK_PROB}
  AFFINITY="--mca pml ucx -x UCX_PROTO_ENABLE=n -x UCX_ROCM_COPY_LAT=2e-6 -x UCX_ROCM_IPC_MIN_ZCOPY=4096 ${QUEST_ROOT}/scripts/slurm_affinity_mi300a.sh"
  SRUN="${OMPI_PATH}/bin/mpirun"
fi  

if [[ "${PROFILER}" == "rocprofv3_stats" ]]; then
  stats_dir=${WORK_DIR}/stats
  mkdir ${stats_dir}
  PROFILER_CMD="$QUEST_ROOT/scripts/rocprofv3_mpi_wrapper.sh $stats_dir results --kernel-trace --stats --truncate-kernels --"
else
  PROFILER_CMD=""
fi

module list
echo "QUEST_SYSTEM=${QUEST_SYSTEM}"
echo "QUEST_EXEC=${QUEST_EXEC}"
echo "N_QUBIT=${N_QUBIT}"
echo "PROFILER_CMD=${PROFILER_CMD}"


# Use blitz kernels instead of SDMA
export HSA_ENABLE_SDMA=0

RUN_CMD="${SRUN} -n ${N_MPI} ${AFFINITY} ${PROFILER_CMD} ${QUEST_EXEC} ${N_QUBIT} |& tee ${WORK_DIR}/app_output.log" 
echo -e "Run command: ${RUN_CMD}" 

eval ${RUN_CMD}