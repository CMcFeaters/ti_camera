"""
builds the shared mem, run this before mp1, keep it alive till mp2 finishes
when killing it use ctrl+c and it will spit out the list
"""

from multiprocessing import shared_memory
from time import sleep
shm_a = shared_memory.SharedMemory(create=True, size=10, name="test")
print(type(shm_a.buf))

buffer = shm_a.buf
buffer[:10] = bytearray([0 for i in range(10)])  # Modify multiple at once
shm_a.buf[4] = 100                           # Modify single byte at a time

print(shm_a.buf[4])
try:
	while 1:
		sleep(1)
except KeyboardInterrupt:
	print("closing")
	for thing in shm_a.buf:
		print(thing)
	shm_a.close()
	shm_a.unlink()
	
	