import numpy as np

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