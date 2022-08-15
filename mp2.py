"""
meant to run second after mp1.
This is intended to modify buffer spot 4 of the "test" document
shoudl be run:
python ./mp2.py [some number]
"""

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

	
	