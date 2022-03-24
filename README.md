# MPI_Bucket_Sort

### Simple Overview of Algorithm
1. Array of random Numbers is created on main process (process 0)
2. Array is segmented, and partitioned to each of the available processes
3. Each process groups the values of their array segment into "buckets" by value.
   - Each bucket represents some bound of integer value EX.(10-20)
4. Every bucket on every process is then sorted individually
5. Buckets across processes with the same bounds, are aggregated to the process matching their bucket indices.
   - For example: Given 3 processes with the buckets (1-10), (11-20), and (21-30), process 0 will receive the buckets holding (1-10) from the other 2 processes. 
6. These aggregated arrays are then sorted on each of the processes. 
7. All values are then merged back into a single array on the main process (process 0). 

### Requirements
- Python 2.7, 3.5 or above
- mpi4py
  - python -m pip install mpi4py

### Usage
#### mpirun -n 8 --mca mpi_cuda_support 0 python BucketSortDemo.py