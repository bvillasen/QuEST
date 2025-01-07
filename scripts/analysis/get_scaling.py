
import numpy as np
import tools
import importlib
importlib.reload(tools)

problem = 1
n_qubit = 33
n_mpi = 4

memory_size_GB, memory_size_per_rank_GB, vector_size_per_rank_GB = tools.get_memory_size( n_qubit, n_mpi )
mpi_transfer_size_GB = tools.get_mpi_transfer_size( problem, n_qubit, n_mpi )

print( f'Problem: {problem}  n_qubit: {n_qubit}  n_mpi: {n_mpi}')
print( f'MPI transfer size: {mpi_transfer_size_GB} GB')