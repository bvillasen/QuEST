import os, sys
import numpy as np
import tools
import importlib
importlib.reload(tools)

cwd = os.getcwd()
indx = cwd.find('/analysis')
base_data_dir = f'{cwd[:indx]}/KISTI/results_log_files'

problem = 2
n_qubit = 33
n_nodes = 1

  
# Load MI250X data
gpu_type = 'mi250x'
n_mpi = 8
data_dir = f'{base_data_dir}/{gpu_type}/problem_{problem}'
rocprof_dir = f'{data_dir}/rocprofv3_nqubit{n_qubit}_nnodes{n_nodes}_nmpi{n_mpi}/'
stats_all_mi250x = tools.load_rocprof_stats( n_mpi, rocprof_dir )
kernel_stats_p1_mi250x = tools.concatenate_kernel_stats( stats_all_mi250x )  
  
# Load MI300A data
gpu_type = 'mi300a'
n_mpi = 4
data_dir = f'{base_data_dir}/{gpu_type}/problem_{problem}'
rocprof_dir = f'{data_dir}/rocprofv3_nqubit{n_qubit}_nnodes{n_nodes}_nmpi{n_mpi}/'
stats_all_mi300a = tools.load_rocprof_stats( n_mpi, rocprof_dir )
kernel_stats_p1_mi300a = tools.concatenate_kernel_stats( stats_all_mi300a )  

kernel_stats = kernel_stats_p1_mi250x
for k_id in kernel_stats_p1_mi250x:
  k_data_mi250x = kernel_stats_p1_mi250x[k_id]
  k_name = k_data_mi250x['Name']
  n_calls_mi250x = k_data_mi250x['Calls'].mean()
  total_time_mi250x = k_data_mi250x['TotalDurationNs'].mean()
  kernel_time_mi250x = total_time_mi250x / n_calls_mi250x / 1e6 #millisecs
  k_data_mi300a = tools.get_kernel_data( k_name, kernel_stats_p1_mi300a )
  n_calls_mi300a = k_data_mi300a['Calls'].mean()
  total_time_mi300a = k_data_mi300a['TotalDurationNs'].mean()
  kernel_time_mi300a = total_time_mi300a / n_calls_mi300a / 1e6 #millisecs
  print( f'{k_id} {k_name:<30}  time_mi250x: {kernel_time_mi250x:.2f}  time_mi300a: {kernel_time_mi300a:.2f}  ratio: {kernel_time_mi250x/kernel_time_mi300a:.2f}  n_mi250x: {n_calls_mi250x}  n_mi300a: {n_calls_mi300a}' )
  
