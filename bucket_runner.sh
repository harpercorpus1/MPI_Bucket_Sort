#!/bin/bash

if [ $# -lt 1 ]; then 
    echo "Executing Bucket Sort on 8 processes"
    mpirun -n 8 --mca mpi_cuda_support 0 python BucketSortDemo.py
elif [ $# -eq 1 ]; then
    echo "Executing Bucket Sort on [$1] processes"
    mpirun -n $1 --mca mpi_cuda_support 0 python BucketSortDemo.py
else
    echo "Usage [./bucket_runner.sh [optional process count]]"
fi