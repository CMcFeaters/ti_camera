from shared_memory_dict import SharedMemoryDict
import time
smd=SharedMemoryDict(name='t1', size=1024)
smd['key1']='you did it'
while 1:
	time.sleep(1)