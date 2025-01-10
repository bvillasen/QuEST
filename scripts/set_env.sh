#!/bin/bash

echo -e "Setting environment for system: ${SYSTEM}"

if [[ "${SYSTEM}" = "lockhart_cpu" ]]; then
  echo "Setting up for CPU-only runs."
  export QUEST_CPU_ONLY=1

elif [[ "${SYSTEM}" = "lockhart_mi250x" ]]; then
  module load rocm/6.2.2
  # module load cray-mpich
  module load cray-mpich/8.1.28
  module load craype-accel-amd-gfx90a
  export MPICH_GPU_SUPPORT_ENABLED=1
  module load cray-pals
  export QUEST_GPU_ARCH="gfx90a"
  export QUEST_GPU_TYPE="mi250x"
  export QUEST_CC=cc
  export QUEST_CXX=CC

elif [[ "${SYSTEM}" = "lockhart_mi300a" ]]; then
  module load rocm/6.2.1
  module load cray-mpich
  # module load cray-mpich/8.1.28 
  module load craype-accel-amd-gfx942
  module load cray-pals
  export MPICH_GPU_SUPPORT_ENABLED=1
  export QUEST_GPU_ARCH="gfx942"
  export QUEST_GPU_TYPE="mi300a"
  export QUEST_CC=cc
  export QUEST_CXX=CC

elif [[ "${SYSTEM}" = "pp_conductor" ]]; then
  export ROCM_PATH=/opt/rocm-6.3.0
  export OMPI_PATH=/opt/ompi-5.0.3
  export QUEST_GPU_ARCH="gfx942"
  export QUEST_GPU_TYPE="mi300a"  
  export QUEST_CC=$OMPI_PATH/bin/mpicc
  export QUEST_CXX=$OMPI_PATH/bin/mpicxx

else
  echo -e "System: ${SYSTEM} not in list of known systems. "
  return
fi

export QUEST_SYSTEM=${SYSTEM}

if [[ -v QUEST_ROOT ]]; then
    echo "QUEST_ROOT: ${QUEST_ROOT}"
else
  CURRENT_DIR=$(pwd)
  if [[ "$CURRENT_DIR" == *"QuEST"* ]]; then
    prefix=${CURRENT_DIR%%"QuEST"*}
    index=$(( ${#prefix} ))
    export QUEST_ROOT="${CURRENT_DIR:0:index}QuEST"
    echo -e "QUEST_ROOT: ${QUEST_ROOT}" 
  else
    echo -e "ERROR: QUEST_ROOT directory couldn't be find"
    echo -e "Set the path manually by setting: export QUEST_ROOT=<path to QuEST repository"
    return
  fi
fi