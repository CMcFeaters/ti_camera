'''
A program that is called by the PHP file.  This program asks the TI_client to take a pic and then 
returns the file name of that pic to the php file.
This prgram:
-Receives request from php
-writes request info to SDM 'request'
-waits for a file name in SDM 'response'
-writes '' to SDM 'response'
'''

from shared_memory_dict import SharedMemoryDict
from time import sleep
import sys

#This value will be provided by the calling php function, it will be the IP address
who=str(sys.argv[1])

#establisih shared mem dict and fill in our request
exist_smd=SharedMemoryDict(name='queue', size=1024)
exist_smd[who]=1

#well our request has not been filled, wait
while exist_smd[who]==1:
	sleep(1)
	
#onece our request is filled, return the value (shoudl be file name)
print (exist_smd[who])
exist_smd.shm.close()
