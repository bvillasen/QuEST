#!/bin/bash

if [[ -n ${OMPI_COMM_WORLD_LOCAL_RANK+z} ]]; then  
    export MPI_RANK=${OMPI_COMM_WORLD_LOCAL_RANK}   
    export MPI_SIZE=${OMPI_COMM_WORLD_LOCAL_SIZE} 
elif [[ -n "${SLURM_LOCALID+z}" ]]; then 
    export MPI_RANK=${SLURM_LOCALID} 
    export MPI_SIZE=${SLURM_NTASKS_PER_NODE}
    # export MPI_SIZE=${SLURM_NTASKS}
fi 
echo "MPI_RANK: $MPI_RANK  MPI_SIZE: $MPI_SIZE" 


if [ -z "${OMP_NUM_THREADS}" ]; then
    let OMP_NUM_THREADS=1
fi

if [ -z "${RANK_STRIDE}" ]; then
    let RANK_STRIDE=24
fi

if [ -z "${OMP_STRIDE}" ]; then
    let OMP_STRIDE=1
fi

if [ -z "${NUM_GPUS}" ]; then
    let NUM_GPUS=4
fi

if [ -z "${CPU_SHIFT}" ]; then
    let CPU_SHIFT=0
fi

if [ -z "${GPU_START}" ]; then
    let GPU_START=0
fi

if [ -z "${GPU_STRIDE}" ]; then
    let GPU_STRIDE=1
fi

# APU_LIST=(2 3 0 1)
APU_LIST=(0 1 2 3)

export OMP_NUM_THREADS=${OMP_NUM_THREADS}

let ranks_per_gpu=$(((${MPI_SIZE}+${NUM_GPUS}-1)/${NUM_GPUS}))
echo $ranks_per_gpu
let my_gpu=$(($MPI_RANK*$GPU_STRIDE/$ranks_per_gpu))+${GPU_START}

let cpu_start=$(($RANK_STRIDE*$MPI_RANK))+${GPU_START}+${CPU_SHIFT}
let cpu_stop=$(($cpu_start+$OMP_NUM_THREADS*$OMP_STRIDE-1))
export GOMP_CPU_AFFINITY=$cpu_start-$cpu_stop:$OMP_STRIDE
#export OMP_PLACES="{$cpu_start:$OMP_NUM_THREADS:$OMP_STRIDE}"

export HIP_VISIBLE_DEVICES=${APU_LIST[$my_gpu]}


echo "rank_local= " $MPI_RANK "  GOMP_CPU_AFFINITY= " $GOMP_CPU_AFFINITY "  HIP_VISIBLE_DEVICES= " $HIP_VISIBLE_DEVICES
#echo "rank_local= " $MPI_RANK "  OMP_PLACES= " $OMP_PLACES "  HIP_VISIBLE_DEVICES= " $ROCR_VISIBLE_DEVICES

#prof_name=motorBike_piso_P

#eval "${ROCM_PATH}/bin/rocprof --hsa-trace  --roctx-trace   -d ${prof_name}.${OMPI_COMM_WORLD_RANK} -o ${prof_name}.${OMPI_COMM_WORLD_RANK}/${prof_name}.${OMPI_COMM_WORLD_RANK}.csv $*"

$@