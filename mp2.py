from multiprocessing import shared_memory
from time import sleep
import sys
shm_b = shared_memory.SharedMemory(name="test")
print(type(shm_b.buf))

print(shm_b.buf[4])
shm_b.buf[4]=int(sys.argv[1])
print(shm_b.buf[4])
print("closing")
shm_b.close()

	
	