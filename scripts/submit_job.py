import os
import sys
import shutil
import time
import argparse
import slurm_templates as slurm_templates   

QUEST_ROOT = os.getenv('QUEST_ROOT', None)
if not QUEST_ROOT:
  print("The QUEST_ROOT environment variable should be set ")
  print("Did you remember to `source scripts/set_env.sh` in the QuEST directory ?")
  sys.exit(1)

n_hrs = 0
n_threads_per_core = 1

parser = argparse.ArgumentParser( description="QuEST SLURM script generator.")
parser.add_argument('--system', dest='system', type=str, help='System for the run.', default=None )
parser.add_argument('--problem', dest='problem', type=int, help='Benchmark problem to run [1 or 2]', default=None )
parser.add_argument('--n_qubit', dest='n_qubit', type=int, help='Number of nodes for the run.', default=None )
parser.add_argument('--n_nodes', dest='n_nodes', type=int, help='Number of nodes for the run.', default=1 )
parser.add_argument('--n_mpi', dest='n_mpi', type=int, help='Number of MPI ranks for the run.', default=1 )
parser.add_argument('--work_dir', dest='work_dir', type=str, help='Path of the work directory.', default=None )
parser.add_argument('--use_nodes', dest='use_nodes', nargs='+', help='List of nodes to use for the run.', default=None )
parser.add_argument('--exclude_nodes', dest='exclude_nodes', nargs='+', help='List of nodes to exclude for the run.', default=None )
args = parser.parse_args()

system = args.system
if system is None:
  print( 'ERROR: parameter `--system` has to be specified ')
  exit(1)

problem = args.problem
if problem is None:
  print( 'ERROR: parameter `--problem` has to be specified [1 or 2] ')
  exit(1)

n_qubit = args.n_qubit
if n_qubit is None:
  print( 'ERROR: parameter `--n_qubit` has to be specified ')
  exit(1)

work_dir = args.work_dir
if work_dir is None:
  print( 'ERROR: parameter `--work_dir` has to be specified ')
  exit(1)

n_nodes = args.n_nodes
n_mpi_per_node = args.n_mpi
n_mpi_total = n_nodes * n_mpi_per_node
job_name = f'Q{problem}_n{n_qubit}' 
use_nodes = args.use_nodes
exclude_nodes = args.exclude_nodes

if not os.path.isdir(work_dir): os.mkdir(work_dir)
run_dir = f'{work_dir}/run_nqubit{n_qubit}_nnodes{n_nodes}_nmpi{n_mpi_total}'
if not os.path.isdir(run_dir): os.mkdir(run_dir)
work_dir = run_dir

if system == 'lockhart_cpu':
  slurm_template = slurm_templates.lockhart
  slurm_partition = ""
  n_gpu_per_node = 0
  slurm_options = ''
elif system == 'lockhart_mi250x':
  slurm_template = slurm_templates.lockhart
  slurm_partition = ""
  n_gpu_per_node = 8
  slurm_options = ''
elif system == 'lockhart_mi300a':
  slurm_template = slurm_templates.lockhart
  slurm_partition = '#SBATCH -p MI300'
  n_gpu_per_node = 4
  slurm_options = ''
else: 
  print(f'ERROR: System {system} is not supported.')
  exit(1)

if use_nodes is not None:
  nodes_list = ''
  for node in use_nodes:
    nodes_list += f'{node},'
  slurm_options += f'#SBATCH -w {nodes_list[:-1]} \n'

if exclude_nodes is not None:
  nodes_list = ''
  for node in exclude_nodes:
    nodes_list += f'{node},'
  slurm_options += f'#SBATCH --exclude {nodes_list[:-1]} \n'

print(f'system: {system}' )
print(f'problem: {problem}' )
print(f'n_qubit: {n_qubit}' )
print(f'n_nodes: {n_nodes}' )
print(f'n_mpi_per_node: {n_mpi_per_node}' )
print(f'use_nodes: {use_nodes}' )
print(f'exclude_nodes: {exclude_nodes}' )



set_env_command = f'''
# Set the QuEST environment
export QUEST_ROOT={QUEST_ROOT}
SYSTEM={system} source {QUEST_ROOT}/scripts/set_env.sh
'''

app_run_cmd = '''
# Call application run script
echo "Starting app run. $(date)"
BENCHMARK_PROB=PROBLEM N_QUBIT=NQUBIT N_MPI=NMPI WORK_DIR=WORKDIR bash ${QUEST_ROOT}/scripts/run_app.sh
echo "Finished app run. $(date)"
'''


if problem == 2:
  n_qubit = ( n_qubit - 1 ) // 2
  print( f'WARNING: Redefining n_qubit for problem 2. n_qubit={n_qubit} ')

slurm_script_content = set_env_command
slurm_script_content += app_run_cmd


slurm_script = slurm_template 
slurm_script = slurm_script.replace( 'SLURM_SCRIPT_CONTENT', slurm_script_content)
slurm_script = slurm_script.replace( 'SBATCH_PARTITION', slurm_partition )
slurm_script = slurm_script.replace( 'JOB_NAME', job_name )
slurm_script = slurm_script.replace( 'PROBLEM', str(problem) )
slurm_script = slurm_script.replace( 'NMPI', str(n_mpi_total) )
slurm_script = slurm_script.replace( 'NQUBIT', str(n_qubit) )
slurm_script = slurm_script.replace( 'N_HRS', str(n_hrs) )
slurm_script = slurm_script.replace( 'N_NODES', str(n_nodes) )
slurm_script = slurm_script.replace( 'N_TASK_PER_NODE', str(n_mpi_per_node) )
slurm_script = slurm_script.replace( 'N_GPU_PER_NODE', str(n_gpu_per_node) )
slurm_script = slurm_script.replace( 'N_THREADS_PER_CORE', str(n_threads_per_core) )
slurm_script = slurm_script.replace( 'SLURM_OPTIONS', slurm_options )
slurm_script = slurm_script.replace( 'WORKDIR', work_dir )


file_name = f'{work_dir}/submit_job.slurm'
file = open( file_name, 'w' )
file.write( slurm_script )
file.close()
time.sleep(0.5)
print(f'Saved file: {file_name}')

submit_cmnd = f'sbatch {file_name}'
print( f'Submitting job: {file_name}' )
os.system( submit_cmnd )

