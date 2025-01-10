import numpy as np


def get_kernel_calls( kernel_name, problem, n_qubit, n_mpi ):
  log2_mpi = np.log2(n_mpi)
  if problem == 1:
    if kernel_name == 'statevec_pauliXKernel': return 30*( n_qubit - log2_mpi - 1 ) + 1
    elif kernel_name == 'statevec_controlledNotKernel': return 30*( n_qubit - log2_mpi - 1 ) 
    elif kernel_name == 'statevec_pauliXDistributedKernel': return 30*log2_mpi 
    elif kernel_name == 'statevec_controlledNotDistributedKernel': return 30*log2_mpi
    else: 
      # print( f"ERROR: invalid kernel for problem 1: {kernel_name}")
      return 
  if problem == 2:
    M = ( n_qubit - 1) / 2 
    L = log2_mpi*( n_qubit -1 )  
    if kernel_name == 'statevec_controlledNotKernel': return 2*M*M - L
    elif kernel_name == 'statevec_controlledCompactUnitaryKernel': return (2*M*M - L)/2
    elif kernel_name == 'statevec_hadamardKernel': return n_qubit - log2_mpi + 1
    elif kernel_name == 'statevec_controlledCompactUnitaryDistributedKernel': return L/2
    elif kernel_name == 'statevec_controlledNotDistributedKernel': return L
    elif kernel_name == 'statevec_hadamardDistributedKernel': return log2_mpi
    else: 
      # print( f"ERROR: invalid kernel for problem 2: {kernel_name}")
      return       
    
def get_memory_size( n_qubit, n_mpi):
  n_amps = 2**n_qubit
  vector_size = n_amps * 2 * 8 /1024**3 # Amplitudes vector size in GB
  vector_size_per_rank = vector_size / n_mpi
  memory_size = vector_size
  memory_size_per_rank = vector_size_per_rank
  if n_mpi > 1: 
    memory_size *= 2 # Extra array for MPI communication
    memory_size_per_rank *= 2 # Extra array for MPI communication
  memory_size_per_rank = memory_size / n_mpi
  return memory_size, memory_size_per_rank, vector_size_per_rank


def get_mpi_transfer_size( problem, n_qubit, n_mpi ):
  log2_mpi = np.log2(n_mpi)
  memory_size_GB, memory_size_per_rank_GB, vector_size_per_rank_GB = get_memory_size( n_qubit, n_mpi )
  if problem ==1: 
    n_exchange_vector = 2 * 30 * log2_mpi
  if problem == 2:
    n_exchange_vector =  log2_mpi*(n_qubit-1)*(1 + 1/2) + log2_mpi
  return n_exchange_vector * vector_size_per_rank_GB



def load_amplitudes( base_dir, n_mpi ):
  import h5py as h5
  
  amps = None
  for rank in range(n_mpi):
    file_name = base_dir + f'/amps_id_{rank}.h5'
    print( f'Loading file: {file_name}')
    file = h5.File( file_name, 'r' )
    if amps is None:
      n_amps_local = int(file.attrs['numAmpsPerChunk'][0])
      amps = {}
      amps['real'] = np.zeros(n_amps_local*n_mpi, dtype=float)
      amps['imag'] = np.zeros(n_amps_local*n_mpi, dtype=float)
    real = file['amps_real'][...]
    imag = file['amps_imag'][...]
    start = rank*n_amps_local
    end = (rank+1)*n_amps_local
    amps['real'][start:end] = real
    amps['imag'][start:end] = imag
  return amps

def parse_run_output( run_dir, data_dir ):
  run_name = run_dir.split('_')
  n_qubit = int(run_name[1][6:])
  n_nodes = int(run_name[2][6:])
  n_mpi = int(run_name[3][4:])
  print( f'Loading {run_dir}   n_qubit: {n_qubit}  n_nodes: {n_nodes}  n_mpi: {n_mpi}')
  # run_file_name = f'{data_dir}/{run_dir}/job_output.log'
  run_file_name = f'{data_dir}/{run_dir}/app_output.log'
  file = open( run_file_name, 'r' )
  lines = file.readlines()
  time_alloc, time_circuit, time_dealloc = 0, 0, 0
  time_mpi_min, time_mpi_max, time_mpi_mean = 0, 0, 0
  size_mpi_min, size_mpi_max, size_mpi_mean = 0, 0, 0
  bw_mpi_min, bw_mpi_max, bw_mpi_mean = 0, 0, 0
  for line in lines:
    # print(line)
    if line.find('Alloc') == 0: time_alloc = float(line.split(' ')[3]) 
    if line.find('Circuit Op') == 0: 
      circuit = line.split('           ')[1]
      time_circuit = float(circuit.split(' ')[0]) 
    if line.find('Deallocation') == 0: 
        dealloc = line.split('                ')[1]
        time_dealloc = float(dealloc.split(' ')[0]) 
    if line.find('MPI time') == 0:
      times = line.split('  ')
      time_mpi_min = float(times[0].split(' ')[3])
      time_mpi_max = float(times[1].split(' ')[2])
      time_mpi_mean = float(times[2].split(' ')[1])
    if line.find('MPI transfer size') == 0:
      size = line.split('  ')
      size_mpi_min  = float(size[0].split(' ')[4])
      size_mpi_max  = float(size[1].split(' ')[2])
      size_mpi_mean = float(size[2].split(' ')[1])
    if line.find('MPI Bandwidth') == 0:
      bw = line.split('  ')
      bw_mpi_min  = float(bw[0].split(' ')[5])
      bw_mpi_max  = float(bw[1].split(' ')[2])
      bw_mpi_mean = float(bw[2].split(' ')[1])      
  file.close()
  data = {'n_qubit':n_qubit, 'n_node':n_nodes, 'n_mpi':n_mpi,
          'time_alloc':time_alloc, 'time_circuit':time_circuit, 'time_dealloc':time_dealloc,
          'time_mpi_min':time_mpi_min, 'time_mpi_max':time_mpi_max, 'time_mpi_mean':time_mpi_mean,
          'size_mpi_min':size_mpi_min, 'size_mpi_max':size_mpi_max, 'size_mpi_mean':size_mpi_mean,
          'bw_mpi_min':bw_mpi_min, 'bw_mpi_max':bw_mpi_max, 'bw_mpi_mean':bw_mpi_mean    }
  return data

def concatenate_data( data, skip_nmpi_1=False ):
  data_all = {}
  for i in data:
    run_data = data[i]
    if skip_nmpi_1:
      if run_data['n_mpi'] < 2: continue
    for key in run_data:
      if key not  in data_all: data_all[key] = []
      data_all[key].append( run_data[key])
  for key in data_all: data_all[key] = np.array(data_all[key])
  return data_all



def load_rocprof_results( file_name, load_with='pandas' ):
  import pandas as pd
  print( f'Loading file: {file_name}' )
  if load_with == 'pandas':
    df = pd.read_csv( file_name )
    return df

def load_rocprof_stats( n_mpi, rocprof_dir ):
  stats_all = {}
  for rank in range(n_mpi):
    rocprof_file = f'{rocprof_dir}/stats/rank_{rank}/results_kernel_stats.csv'
    rocprof_stats = load_rocprof_results( rocprof_file )
    stats_all[rank] = rocprof_stats
  return stats_all

def concatenate_kernel_stats( stats_all ):
  keys = ['Calls', 'TotalDurationNs']
  kernel_names = stats_all[0]['Name'].values

  data_kernels = {}
  for k_id, k_name in enumerate(kernel_names):
    data_kernels[k_id] = { 'Name': k_name }
    for rank_id in stats_all:
      df = stats_all[rank_id]
      k_data = df[df['Name'] == k_name ]
      for key in keys:
        if key not in data_kernels[k_id]: data_kernels[k_id][key] = []
        data_kernels[k_id][key].append( k_data[key].values[0] )
    for key in keys: data_kernels[k_id][key] = np.array(data_kernels[k_id][key])
  return data_kernels



def get_kernel_data( kernel_name, data_kernels ):
  counter = 0
  for i in data_kernels:
    if data_kernels[i]['Name'] == kernel_name: 
      counter += 1
      kernel_data = data_kernels[i]
  if counter == 1: return kernel_data
  if counter == 0: print( f"ERROR: Kernel {kernel_name} nor found")
  if counter > 1: print( f"ERROR: More than one kernel with name {kernel_name} found")
