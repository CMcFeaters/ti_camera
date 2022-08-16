#!/home/pi/tienv/bin/python3

'''
A program that is called by the PHP file.  This program asks the TI_client to take a pic and then 
returns the file name of that pic to the php file.
This prgram:
-Receives request from php
-writes a requests to 
-waits for a file name in client_cam 'response'
-returns filename to php file
'''
from time import sleep
import sys
import redis

#This value will be provided by the calling php function, it will be the IP address
if len(sys.argv)>1:
	who="IP:"+str(sys.argv[1])
else:
	who="IP:123"
print (who)

#establisih shared mem dict and fill in our request
r = redis.Redis(host='localhost', port=6379, db=0)
r.set (who,"open")

#well our request has not been filled, wait
while r.get(who)==b"open":
	sleep(1)

fname=r.get(who).decode("utf-8")
r.set(who,"closed")
r.delete(who)
#onece our request is filled, return the value (shoudl be file name)
print (fname)

