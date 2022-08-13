#1/home/i/env/bin/python3

'''
This program is the client runs on the NAS.  It activates on its own every 60 and 70s or when requested to via the php program.
This program:
-tracks when 60/70s have occured to take a pic
-checks an SDM 'request' for a pic request
-Send a request to the PIcam to take a pic
-Receives that data from picam
-WRites the data to a file
-if on demand, writes that filename to SDM 'response'
-writes '' to SDM 'request'

Server: PiCamera 192.168.1.227
Client: PiNAS 192.168.1.9

'''

from time import sleep
from datetime import datetime as dt
import cv2
import socket
import numpy as np
import os
from shared_memory_dict import SharedMemoryDict

#ip info
HOST = "192.168.1.227"	#basic loopback for local host
PORT=65432	#non-privileged port
PIC_TIME=3	#we are saying 3s for a picture to be taken
LOW_TIME=55	#time for our first pic
HIGH_TIME=66 #time for our second pic

#the shared memory dict we will use for instant requests
smd=SharedMemoryDict(name='queue', size=1024)


def main_loop():
	"""
	main_loop(): takes a picture rougly every 55/65s and whenever someone requests a picture be taken
	1) checks time to see if it's picture time.  if it is, 
	-take a pic and increment time.
	-if it's 65, reset timer to 0
	2) check the shared memory queue to see if any ip addresses have requested a pic (e.g. dict[key]==1
	-if they have, take a pic
	-write the filename to the SMD[ip]
	3) if neither of those are true, increment the counter
	
	returns: nothing
	"""
	t=0
	while 1:
		if t>=HIGH_TIME:	#if we are over 63s, take a pic and reset our timer
			t=0
			request_pic()
		elif t==LOW_TIME:	#are we at 55s?  If so take a pic 
			'''
			it's ok if this one fails, the reason it woudl do so woudl be we took a requested pic 
			within 3s of 55s, so that's good enough for this program
			'''
			request_pic()
			t+=PIC_TIME
		else:
			time.sleep(1)	#sleep for roughly a second, increment and go
			t+=1
		
		#see if we have any requests, if we do assume it took 3s to fullfill
		if scan_smd()>0:
			t+=PIC_TIME
			
		
		
def scan_smd():
	"""
	scan_smd(): this fucntion is responsible for scanning the SMD and taking pics as requested by:
	1) scan each key in SMD and determine if any values are 1s
	2) if any values are 1s take and store the picture
	3) for each value that was a 1, write the filename
	returns: (int) number of requests fullfilled
	"""
	keylist=[]
	#search to see if we have any requests
	for key in smd.keys():
		if smd[key]==1:
			keylist.append(key)
	
	if len(keylist)>0:	#we have some requests
		fname=request_pic()	#take the pic and save the fname
		#for each requestor, update the smd dict with the filename
		for thing in keylist:
			smd[thing]=fname
		
		return len(keylist)#return howmany we did
	else:	#we have no requests
		return 0

def request_pic():
	"""
	request_pic:
	1) initiates a socket connection with the pi_cam host
	2) waits and recieves RGB array data back from host
	3) converts to jpg formt
	4) writes to a date/time stamped file
	5) returns the file name
	
	returns: (string) filename 
	"""
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		
		#ask for a picture from the server
		print("Initiating connection")
		s.connect((HOST,PORT))
		s.sendall(b'TI Pic please')
		
		#once we connect, recieve the response until connection is closed
		data=0
		data=s.recv(1024)	#our buffer is 1024 bytes
		i=0
		print ('Receiving file')
		while 1:
			#print('Receiving %d'%i)
			tdata=s.recv(1024)
			if not tdata: break	#if there's nothing here, break out
			data+=tdata
			i+=1
		print("File %d received"%i)
		
		#Write the received data to a file
		#the following lines are magic i copied from somewhere on the internet
		encoded_array=np.fromstring(data,np.uint8)	#convert from string to array
		decoded_image=cv2.imdecode(encoded_array,cv2.IMREAD_COLOR)	#decode arryay to image
		fname='TI_%s.jpg'%dt.now().strftime("%Y%m%d_%H%M%S")
		st1=('/mnt/raid1/shared/TI_20220812/%s'%fname)	#file location
		cv2.imwrite(st1,decoded_image)	#write teh file
		print("File %s written"%st1)
		
		s.close()	#close the socket
	
	#return the file name
	return fname

#if i'm the main dog, run this
if __name__=="__main__":
	main_loop()