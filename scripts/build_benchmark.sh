#!/bin/bash

MAKE_N=8

if [[ -z "${QUEST_ROOT}" ]]; then
  echo -e "The QUEST_ROOT environment variable should be set"
  echo "Did you remember to `source scripts/set_env.sh` in the QuEST directory ?"
  return
fi



if [[ "${PROBLEM}" = "1" ]]; then
  echo "Building KISTI Problem 1"
  BENCHMARK_SRC=${QUEST_ROOT}/kisti_benchmarks/problem_1.c
elif [[ "${PROBLEM}" = "2" ]]; then
  echo "Building KISTI Problem 2"
  BENCHMARK_SRC=${QUEST_ROOT}/kisti_benchmarks/problem_2.c
else 
  echo "Invalid problem number set. Use PRPOBLEM=1 or PRPOBLEM=2 to select which KISTI problem to build."
  exit
fi  

QUEST_BUILD=${QUEST_ROOT}/build_${QUEST_GPU_TYPE}
if [[ ! -d ${QUEST_BUILD} ]]; then
  mkdir ${QUEST_BUILD}
fi
cd ${QUEST_BUILD}

echo "Building benchmark here: ${QUEST_BUILD}"

if [[ -v QUEST_CPU_ONLY ]]; then
  # Build the CPU version of QuEST
  cmake .. -DCMAKE_C_COMPILER=cc -DCMAKE_CXX_COMPILER=CC    \
    -DDISTRIBUTED=1 -DGPUACCELERATED=0 -DMULTITHREADED=ON   \
    -DUSER_SOURCE=${BENCHMARK_SRC} -DOUTPUT_EXE=quest_problem_${PROBLEM}_cpu 
else
  # Build the GPU (HIP) version of QuEST
  cmake .. -DCMAKE_C_COMPILER=cc -DCMAKE_CXX_COMPILER=CC               \
    -DDISTRIBUTED=1 -DGPUACCELERATED=1 -DUSE_HIP=ON  -DGPU_MPI=ON      \
    -DGPU_ARCH=${QUEST_GPU_ARCH} -DNO_CPU_ALLOC=ON -DMULTITHREADED=OFF \
    -DUSER_SOURCE=${BENCHMARK_SRC} -DOUTPUT_EXE=quest_problem_${PROBLEM} 
fi

make -j ${MAKE_N}

