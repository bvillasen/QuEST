#!/bin/bash


if [[ -z "${QUEST_ROOT}" ]]; then
  echo -e "The QUEST_ROOT environment variable should be set"
  echo "Did you remember to `source scripts/set_env.sh` in the QuEST directory ?"
  return
fi


if [[ "${QUEST_SYSTEM}" == "lockhart_cpu" ]]; then
  QUEST_EXEC=${QUEST_ROOT}/build/quest_problem_${BENCHMARK_PROB}_cpu
  AFFINITY="-c 1"
elif [[ "${QUEST_SYSTEM}" == "lockhart_mi250x" ]]; then
  QUEST_EXEC=${QUEST_ROOT}/build_mi250x/quest_problem_${BENCHMARK_PROB}
  AFFINITY="--cpu-bind=verbose --cpu-bind=mask_cpu:ff000000000000,ff00000000000000,ff0000,ff000000,ff,ff00,ff00000000,ff0000000000"
elif [[ "${QUEST_SYSTEM}" == "lockhart_mi300a" ]]; then
  QUEST_EXEC=${QUEST_ROOT}/build_mi300a/quest_problem_${BENCHMARK_PROB}
  AFFINITY=${QUEST_ROOT}/scripts/slurm_affinity_mi300a.sh
fi  

module list
echo "QUEST_SYSTEM=${QUEST_SYSTEM}"
echo "QUEST_EXEC=${QUEST_EXEC}"
echo "N_QUBIT=${N_QUBIT}"


# Use blitz kernels instead of SDMA
export HSA_ENABLE_SDMA=0

RUN_CMD="srun -n ${N_MPI} ${AFFINITY} ${QUEST_EXEC} ${N_QUBIT} |& tee ${WORK_DIR}/app_output.log" 
echo -e "Run command: ${RUN_CMD}" 

eval ${RUN_CMD}