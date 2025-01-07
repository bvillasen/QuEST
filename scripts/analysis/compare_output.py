
import numpy as np
import tools
import importlib
importlib.reload(tools)

problem = 2
n_qubit = 23
n_nodes = 1

n_mpi = 1
benchmarks_dir = '/home/bvillase/benchmarks/quest'
base_dir = f'{benchmarks_dir}/mi250x/problem_{problem}/run_nqubit{n_qubit}_nnodes{n_nodes}_nmpi{n_mpi}'
amps_0 = tools.load_amplitudes( base_dir, n_mpi )

n_mpi = 2
benchmarks_dir = '/home/bvillase/benchmarks/quest'
base_dir = f'{benchmarks_dir}/mi250x/problem_{problem}/run_nqubit{n_qubit}_nnodes{n_nodes}_nmpi{n_mpi}'
amps_1 = tools.load_amplitudes( base_dir, n_mpi )

diff_real = np.abs( amps_1['real'] - amps_0['real'])
indices = np.where( amps_0['real'] > 0 )
diff_real[indices] /  amps_0['real'][indices]

diff_imag = np.abs( amps_1['imag'] - amps_0['imag'])
indices = np.where( amps_0['imag'] > 0 )
diff_real[indices] /  amps_0['imag'][indices]

print( f'diff_real.  min: {diff_real.min()}  max: {diff_real.max()}  avg: {diff_real.mean()}')
print( f'diff_imag.  min: {diff_imag.min()}  max: {diff_imag.max()}  avg: {diff_imag.mean()}')