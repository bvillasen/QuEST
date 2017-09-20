# QuEST

A library for simulating operations on sets of qubits. 

Example operations implemented:
* Rotations of a single qubit
* Measure if a single qubit is in the zero or one state
* Two qubit phase gate

## Getting started

With git: clone the root directory to your device

git clone https://github.com/aniabrown/QuEST.git [QuESTHOME]

Without git: download the directory manually

'Clone or download' > 'Download zip'

In the root directory, run a simple 8 qubit example on one node:

Copy the make file and circuit code to your root directory:
```
cp examples/basicTemplate.c .
cp examples/makefile .
```

The default compiler is the gnu compiler. To change to the intel compiler, edit the COMMON CONFIG section at the beginning of makefile in the root directory. Change COMPILER=GNU to COMPILER=INTEL. Then run:

```
make clean
make
./demo 8
```

This will report some information about the size of the system, perform rotations and verify that
the state vector of probability amplitudes is still normalized. 

OpenMP is enabled by default. To change the number of threads used by the program, set the value of OMP_NUM_THREADS before running the program, eg export OMP_NUM_THREADS=16. See examples/ompJob.sh for an example of how to do this in a job submission script.

## Building other examples

There are other examples of codes using the QuEST library in the examples folder. To use one of these,
copy from the examples folder into the root folder, eg:
cp examples/timingDemo.c timingDemo.c

Edit the COMMON CONFIG section at the beginning of makefile. Change MY_FILE_NAME to the name of the file without
any extension, eg MY_FILE_NAME=timingDemo 

Change the name of the executable as desired eg EXE=myProg.

Run with:
```
make clean
make
./myProg [NUMBER OF QUBITS] 
```
To run on arcus-b on one node, use the job submission script examples/ompJob.sh

## Creating a new file from the template

A basic example file is available in examples/basicTemplate.c. The structure of this file is:

```
Initialisation
Rotations
Measurement
2 Qubit phase gate
Cleanup 
```

In general, leave the initialization and cleanup sections and edit the rotations, measurement and phase gate
sections. Further explanations are in the template file. The full list of QuEST library functions that can be used here is listed in qubits.h. 

## Multi node code

To run over several nodes with MPI, edit the COMMON CONFIG section at the beginning of makefile. 

Change USE_MPI=0 to USE_MPI=1.

Run with:
```
make clean
make
mpirun -np [NUMBER OF PROCESSES] ./demo [NUMBER OF QUBITS]
```
To run on arcus-b, use the job submission script examples/mpiJob.sh

Note that the API to the QuEST library is unchanged when running on multiple nodes. The template file basicTemplate.c
is valid for both single and multi node environments. 

## API Documentation

Full documentation is available at https://aniabrown.github.io/QuEST/

The public API is [here](https://aniabrown.github.io/QuEST/qubits_8h.html)


