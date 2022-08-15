from shared_memory_dict import SharedMemoryDict
import time
exist_smd=SharedMemoryDict(name='t1', size=1024)
print(exist_smd['key1'])
exist_smd.shm.cleanup()

