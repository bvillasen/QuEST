#!/bin/bash
set -euo pipefail
# depends on ROCM_PATH being set outside; input arguments are the output directory & the name
outdir="$1"
name="$2"
if [[ -n ${OMPI_COMM_WORLD_RANK+z} ]]; then
# mpich
export MPI_RANK=${OMPI_COMM_WORLD_RANK}
elif [[ -n ${MV2_COMM_WORLD_RANK+z} ]]; then
# ompi
export MPI_RANK=${MV2_COMM_WORLD_RANK}
elif [[ -n ${SLURM_PROCID+z} ]]; then
export MPI_RANK=${SLURM_PROCID}
else
echo "Unknown MPI layer detected! Must use OpenMPI, MVAPICH, or SLURM"
exit 1
fi
rocprof="${ROCM_PATH}/bin/rocprofv3"
pid="$$"
outdir="${outdir}/rank_${MPI_RANK}"
outfile="${name}"
${rocprof} -d ${outdir} -o ${outfile} "${@:3}"
