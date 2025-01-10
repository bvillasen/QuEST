import os, sys
import numpy as np
import tools
import importlib
importlib.reload(tools)

cwd = os.getcwd()
indx = cwd.find('/analysis')
base_data_dir = f'{cwd[:indx]}/KISTI/results_log_files'

problem = 1
n_qubit = 33
n_nodes = 1

# Load MI300A data
gpu_type = 'mi300a'
n_mpi = 4
data_dir = f'{base_data_dir}/{gpu_type}/problem_{problem}'
rocprof_dir = f'{data_dir}/rocprofv3_nqubit{n_qubit}_nnodes{n_nodes}_nmpi{n_mpi}/'
stats_all_mi300a = tools.load_rocprof_stats( n_mpi, rocprof_dir )
kernel_stats_p1_mi300a = tools.concatenate_kernel_stats( stats_all_mi300a )  

# Collect the average kernel execution time from the run
kernel_avrg_times_mi300a = {}
for k_id in kernel_stats_p1_mi300a:
  k_data = kernel_stats_p1_mi300a[k_id]
  k_name = k_data['Name']
  n_calls = k_data['Calls'].mean()
  total_time = k_data['TotalDurationNs'].mean()
  kernel_time = total_time / n_calls / 1e6 #millisecs
  n_analytic = tools.get_kernel_calls( k_name, problem, n_qubit, n_mpi ) 
  # print( f'{k_id} {k_name:<50}  time_mi300a: {kernel_time:.2f}   n_mi300a: {n_calls}   n_analytic: {n_analytic}' )
  if n_analytic is not None:
    kernel_avrg_times_mi300a[k_id] = {'Name':k_name, 'time_per_call_ms':kernel_time }   
  

# Use the average kernel execution times from the run to extrapolate to the target problem size
target_n_qubit = 40
target_n_mpi = 512
total_gpu_kernel_time_p1 = 0
print( f'\nProblem: {problem}  target_n_qubit: {target_n_qubit}  target_n_mpi: {target_n_mpi}')
for k_id in kernel_avrg_times_mi300a:
  kernel_data = kernel_avrg_times_mi300a[k_id]
  kernel_name = kernel_data['Name']
  kernel_time = kernel_data['time_per_call_ms']
  target_n_cals = tools.get_kernel_calls( kernel_name, problem, target_n_qubit, target_n_mpi )
  target_kernel_total_time = target_n_cals * kernel_time / 1e3 #Convert to seconds
  print( f'{k_id} {kernel_name:<50}   target_n_calls: {target_n_cals}  target_kernel_total_time: {target_kernel_total_time:.2f} secs' )
  total_gpu_kernel_time_p1 += target_kernel_total_time
print( f'Total GPU kernel time for problem 1: {total_gpu_kernel_time_p1} secs\n\n')
# Do the same for problem 2

problem = 2
n_qubit = 33
n_nodes = 1

# Load MI300A data
gpu_type = 'mi300a'
n_mpi = 4
data_dir = f'{base_data_dir}/{gpu_type}/problem_{problem}'
rocprof_dir = f'{data_dir}/rocprofv3_nqubit{n_qubit}_nnodes{n_nodes}_nmpi{n_mpi}/'
stats_all_mi300a = tools.load_rocprof_stats( n_mpi, rocprof_dir )
kernel_stats_p1_mi300a = tools.concatenate_kernel_stats( stats_all_mi300a )  

# Collect the average kernel execution time from the run
kernel_avrg_times_mi300a = {}
for k_id in kernel_stats_p1_mi300a:
  k_data = kernel_stats_p1_mi300a[k_id]
  k_name = k_data['Name']
  n_calls = k_data['Calls'].mean()
  total_time = k_data['TotalDurationNs'].mean()
  kernel_time = total_time / n_calls / 1e6 #millisecs
  n_analytic = tools.get_kernel_calls( k_name, problem, n_qubit, n_mpi ) 
  # print( f'{k_id} {k_name:<50}  time_mi300a: {kernel_time:.2f}   n_mi300a: {n_calls}   n_analytic: {n_analytic}' )
  if n_analytic is not None:
    kernel_avrg_times_mi300a[k_id] = {'Name':k_name, 'time_per_call_ms':kernel_time }   
  

# Use the average kernel execution times from the run to extrapolate to the target problem size
target_n_qubit = 39
target_n_mpi = 256
total_gpu_kernel_time_p2 = 0
print( f'\nProblem: {problem}  target_n_qubit: {target_n_qubit}  target_n_mpi: {target_n_mpi}')
for k_id in kernel_avrg_times_mi300a:
  kernel_data = kernel_avrg_times_mi300a[k_id]
  kernel_name = kernel_data['Name']
  kernel_time = kernel_data['time_per_call_ms']
  target_n_cals = tools.get_kernel_calls( kernel_name, problem, target_n_qubit, target_n_mpi )
  target_kernel_total_time = target_n_cals * kernel_time / 1e3 #Convert to seconds
  print( f'{k_id} {kernel_name:<50}   target_n_calls: {target_n_cals}  target_kernel_total_time: {target_kernel_total_time:.2f} secs' )
  total_gpu_kernel_time_p2 += target_kernel_total_time  
print( f'Total GPU kernel time for problem 2: {total_gpu_kernel_time_p2} secs')
