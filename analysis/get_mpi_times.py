import os, sys
import numpy as np
import tools
import importlib
importlib.reload(tools)

cwd = os.getcwd()
indx = cwd.find('/analysis')
base_data_dir = f'{cwd[:indx]}/KISTI/results_log_files'


problem = 1
n_qubit = 40
n_mpi = 512
vector_size_GB = 16 * 2**n_qubit / n_mpi / 1024**3
n_vector_exchange = 60 * np.log2(n_mpi)
transfer_size_per_rank_p1_GB = vector_size_GB * n_vector_exchange

problem = 2
n_qubit = 39
n_mpi = 256
vector_size_GB = 16 * 2**n_qubit / n_mpi / 1024**3
M = (n_qubit - 1 )/2
L = np.log2(n_mpi)*(n_qubit - 1 )
n_vector_exchange = 3/2*L + np.log2(n_mpi)
transfer_size_per_rank_p2_GB = vector_size_GB * n_vector_exchange



