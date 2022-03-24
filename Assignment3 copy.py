"""
Harper Corpus
Multiprocessing Bucket Sort
"""

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD; rank = comm.Get_rank(); size = comm.Get_size()
N = 64

# creates list of random numbers and prints it on rank 0
# it also reshapes the unsorted array to be in segments for each 
# process
if rank == 0:
    original_unsorted_list = np.random.randint(low=1, high=N, size=N)
    print('Original Unsorted List:\n', original_unsorted_list)
    original_unsorted_list = original_unsorted_list.reshape(size, int(N/size))
else:
    original_unsorted_list = None

# sends the partitioned portions of the list to each process
partitioned_list = comm.scatter(original_unsorted_list, root=0)

# initializes numpy arrays to hold the values of the small buckets
# and the lengths of each bucket
small_buckets = np.zeros(size*N, dtype="int").reshape(size, N)
sender_sizes = np.zeros(size, dtype="int")

# loops through each bucket 
for i in partitioned_list:
    for j in range(size):
        # condition for the bounds of the small buckets
        if i > (j * (N / size)) and i <= ((j+1) * (N/size)):
            # adds the value from the list into the small bucket
            small_buckets[j][sender_sizes[j]] = i
            # increases the length of the bucket
            sender_sizes[j] += 1
            break;
            
# value used to shorten the length of the numpy array 
maxLen = max(sender_sizes)
# shortens the length of the small bucket arrays
small_buckets = np.array([i[:maxLen] for i in small_buckets])
# cleans unwanted data from numpy array
small_buckets = small_buckets.flatten()
small_buckets = small_buckets[small_buckets != 0]

# initializes containers for sending/recieving data
reciever_sizes = np.zeros(size, dtype="int")
large_buckets = np.zeros(N, dtype="int")
sender_disp = np.zeros(size, dtype="int")

# sends the number of data members to send to each process to each other
reciever_sizes = comm.alltoall(sender_sizes)

# populates displacement arrays using send_sizes/reciever_sizes
sender_disp = [0]
reciever_disp = [0]
for i in range(1,size):
    sender_disp.append(sender_disp[i-1] + sender_sizes[i-1])
    reciever_disp.append(reciever_disp[i-1] + reciever_sizes[i-1])
  
# sends bucket i on every process to process i for i in (0, size)
comm.Alltoallv([small_buckets, tuple(sender_sizes), tuple(sender_disp), MPI.DOUBLE], [large_buckets, tuple(reciever_sizes), tuple(reciever_disp), MPI.DOUBLE])    

# cleans and sorts data on each process
large_buckets = large_buckets[large_buckets != 0]
large_buckets.sort()

# initializes array used to hold 
if rank == 0:
    full_sorted_list = np.zeros(N, dtype="int")
else:
    full_sorted_list = None

# sends size of bucket to process 0
sizeof_bucket = len(large_buckets)
counts = comm.gather(sizeof_bucket, root=0)

# calculates displacements from each process on process 0
if rank == 0:
    displacements = [0]
    for i in range(1, size):
        displacements.append(counts[i-1] + displacements[i-1])
else:
    displacements = []
    counts = []
 
# Gathers all data on process 0
comm.Gatherv(large_buckets, [full_sorted_list, tuple(counts), tuple(displacements), MPI.DOUBLE])       
# prints the complete sorted list on process 0
if rank == 0:
    print('Complete Sorted List\n', full_sorted_list)

