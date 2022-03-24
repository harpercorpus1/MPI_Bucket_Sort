Loading into the palmetto Cluster using Jupyter Notebook 

Use all defaults except for changing the number of cpus to 8

load necessary modules:
    module load openmpi/4.0.5-gcc/8.3.1-ucx

run the program: 
    mpirun -n 8 --mca mpi_cuda_support 0 python Assignment3.py 

