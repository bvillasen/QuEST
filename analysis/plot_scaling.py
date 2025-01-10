import os, sys
import numpy as np
import tools
import importlib
importlib.reload(tools)


cwd = os.getcwd()
indx = cwd.find('/analysis')
base_data_dir = f'{cwd[:indx]}/KISTI/results_log_files'
output_dir = f'{cwd}/figures/' 


gpu_type = 'mi250x'
problem = 1
data_dir = f'{base_data_dir}/{gpu_type}/problem_{problem}'
run_dirs = [ d for d in os.listdir( data_dir ) if d.find('run')==0 ]
data_p1_mi250x = {}
for i,run_dir in enumerate(run_dirs): data_p1_mi250x[i] = tools.parse_run_output( run_dir, data_dir ) 
data_p1_mi250x_all = tools.concatenate_data( data_p1_mi250x, skip_nmpi_1=True )


gpu_type = 'mi300a'
problem = 1
data_dir = f'{base_data_dir}/{gpu_type}/problem_{problem}'
run_dirs = [ d for d in os.listdir( data_dir ) if d.find('run')==0 ]
data_p1_mi300a = {}
for i,run_dir in enumerate(run_dirs): data_p1_mi300a[i] = tools.parse_run_output( run_dir, data_dir ) 
data_p1_mi300a_all = tools.concatenate_data( data_p1_mi300a )


data_all = data_p1_mi250x_all

import matplotlib.pyplot as plt 

nrows, ncols = 1, 2
h_scale_factor = 0.7
figure_width  = 3 *ncols
figure_height = figure_width * h_scale_factor
font_size = 10
legend_size = 7
fig_text_size = 8

n_figs = nrows * ncols
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,figure_height*nrows))
plt.subplots_adjust( hspace = 0.15, wspace=0.15)

ls_circuit = '-'
ls_gpu = 'dotted'
ls_mpi = '--'

c_mi250x = 'C0'
c_mi300a = 'C2'

ax = ax_l[0]
nqubit_mi250x = data_p1_mi250x_all['n_qubit']
time_circuit_mi250x = data_p1_mi250x_all['time_circuit']
time_mpi_min_mi250x = data_p1_mi250x_all['time_mpi_min']
time_mpi_max_mi250x = data_p1_mi250x_all['time_mpi_max']
time_mpi_mean_mi250x = data_p1_mi250x_all['time_mpi_mean']
time_gpu_mi250x = time_circuit_mi250x - time_mpi_max_mi250x
ax.plot(nqubit_mi250x, time_circuit_mi250x, c=c_mi250x, ls=ls_circuit, label="Bard Peak Time Circuit"  )
ax.fill_between(nqubit_mi250x, time_mpi_min_mi250x, time_mpi_max_mi250x,  color=c_mi250x,  alpha=0.3)
ax.plot(nqubit_mi250x, time_mpi_mean_mi250x, c=c_mi250x, ls=ls_mpi, label="Bard Peak Time MPI"  )
ax.plot(nqubit_mi250x, time_gpu_mi250x, c=c_mi250x, ls=ls_gpu, label='Bard Peak Time GPU'  )

nqubit_mi300a = data_p1_mi300a_all['n_qubit']
time_circuit_mi300a = data_p1_mi300a_all['time_circuit']
time_mpi_min_mi300a = data_p1_mi300a_all['time_mpi_min']
time_mpi_max_mi300a = data_p1_mi300a_all['time_mpi_max']
time_mpi_mean_mi300a = data_p1_mi300a_all['time_mpi_mean']
time_gpu_mi300a = time_circuit_mi300a - time_mpi_max_mi300a

ax.plot(nqubit_mi300a, time_circuit_mi300a, c=c_mi300a, ls=ls_circuit, label="Parry Peak Time Circuit"  )
ax.fill_between(nqubit_mi300a[1:], time_mpi_min_mi300a[1:], time_mpi_max_mi300a[1:],  color=c_mi300a,  alpha=0.3)
ax.plot(nqubit_mi300a[1:], time_mpi_mean_mi300a[1:], c=c_mi300a, ls=ls_mpi, label="Parry Peak Time MPI"  )
ax.plot(nqubit_mi300a, time_gpu_mi300a, c=c_mi300a, ls=ls_gpu, label='Parry Peak Time GPU'  )


ax.grid( color='gray', alpha=0.5)
ax.legend(loc=2, fontsize=legend_size)
ax.set_yscale('log')
ax.set_ylabel( 'Time [secs]')
ax.set_xlabel( 'N qubit')

ax2 = ax.twiny()
ax2.set_xticks(ax.get_xticks())
ax2.set_xbound(ax.get_xbound())
ax2.set_xticklabels([int(2**(x-31)) for x in ax.get_xticks()])
ax2.set_xlabel('N GPUs')

ax = ax_l[1]
bw_per_gpu_min_mi250x = 2*data_p1_mi250x_all['bw_mpi_min']
bw_per_gpu_max_mi250x = 2*data_p1_mi250x_all['bw_mpi_max']
bw_per_gpu_mean_mi250x = 2*data_p1_mi250x_all['bw_mpi_mean']
ax.fill_between(nqubit_mi250x, bw_per_gpu_min_mi250x, bw_per_gpu_max_mi250x, color=c_mi250x, alpha=0.5)
ax.plot(nqubit_mi250x, bw_per_gpu_mean_mi250x, c=c_mi250x, label="Bard Peak Comm BW per GPU"  )

bw_per_gpu_min_mi300a = data_p1_mi300a_all['bw_mpi_min']
bw_per_gpu_max_mi300a = data_p1_mi300a_all['bw_mpi_max']
bw_per_gpu_mean_mi300a = data_p1_mi300a_all['bw_mpi_mean']
ax.fill_between(nqubit_mi300a[1:], bw_per_gpu_min_mi300a[1:], bw_per_gpu_max_mi300a[1:], color=c_mi300a, alpha=0.5)
ax.plot(nqubit_mi300a[1:], bw_per_gpu_mean_mi300a[1:], c=c_mi300a, label="Parry Peak Comm BW per GPU"  )
ax.axhline( y=25, c='C3', lw=0.8, label = 'NIC BW = 25 GB/s')


ax.set_ylabel( 'Communication BW per GPU [GB/s]')
ax.set_xlabel( 'N qubit')
ax.legend(loc=1, fontsize=legend_size)
ax.grid( color='gray', alpha=0.5)

ax2 = ax.twiny()
ax2.set_xticks(ax.get_xticks())
ax2.set_xbound(ax.get_xbound())
ax2.set_xticklabels([int(2**(x-31)) for x in ax.get_xticks()])
ax2.set_xlabel('N GPUs')


figure_name = output_dir + f'problem_1_communication.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


# problem = 1
# n_qubit = 33
# n_mpi = 4

# memory_size_GB, memory_size_per_rank_GB, vector_size_per_rank_GB = tools.get_memory_size( n_qubit, n_mpi )
# mpi_transfer_size_GB = tools.get_mpi_transfer_size( problem, n_qubit, n_mpi )

# print( f'Problem: {problem}  n_qubit: {n_qubit}  n_mpi: {n_mpi}')
# print( f'MPI transfer size: {mpi_transfer_size_GB} GB')