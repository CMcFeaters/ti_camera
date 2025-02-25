#1/home/pi/ti_env/bin/python

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
Server2: PiZero: 192.168.1.247
Client: PiNAS 192.168.1.9

'''

import redis
from time import sleep
from datetime import datetime as dt
from dotenv import dotenv_values
import cv2
import socket
import numpy as np
import os

#ip info
config=dotenv_values(".env_client")
r = redis.Redis(host='localhost', port=6379, db=0)
HOST = config['pi3_host']	#pi camera host
Z_HOST = config['pi0_host'] #pi zero camera host
b_file= "TI_%s_B"%config['gamedate']
p_file= "TI_%s_P"%config['gamedate']
f_dir=config['f_dir']
PORT=65432	#non-privileged port
PIC_TIME=3	#we are saying 3s for a picture to be taken
LOW_TIME=15	#time for our first pic
HIGH_TIME=30 #time for our second pic


def directory_check():
	'''
	checks to verify the directories exist.  if they do not, creates them
	'''
	paths=[os.path.join(f_dir,p_file),os.path.join(f_dir,b_file)]
	for path in paths:
		try: 
			os.mkdir(path)
			print(f"Directory Created '{path}'")
		except FileExistsError:
			print(f"Directory '{path}' already exists.")
		except PermissionError:
			print(f"Permission denied: Unable to create '{path}'.")
		except Exception as e:
			print(f"An error occurred: {e}")

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
			sleep(1)	#sleep for roughly a second, increment and go
			t+=1
		
		#see if we have any requests, if we do assume it took 3s to fullfill
		if scan_redis()>0:
			t+=PIC_TIME
			
		
		
def scan_redis():
	"""
	scan_redis(): this fucntion is responsible for scanning the redis db and taking pics as requested by:
	1) scan each key in redis db and determine if any values are "open"
	2) if any values are "open" take and store the picture
	3) for each value that was a "open", write the filename to that key
	returns: (int) number of requests fullfilled
	"""
	keylist=[]
	#search to see if we have any requests
	for key in r.scan_iter("IP:*"):
		print("%s - %s"%(key,r.get(key)))
		if r.get(key)==b"open":
			keylist.append(key)
	
	if len(keylist)>0:	#we have some requests
		fname=request_pic()	#take the pic and save the fname
		#for each requestor, update the smd dict with the filename
		for thing in keylist:
			r.set(thing,fname)
		
		return len(keylist)#return howmany we did
	else:	#we have no requests
		return 0

def take_pic(host,port,file):
	'''
		initiates the socket given the various inputs
	'''
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	
		#ask for a picture from the server
		print("Initiating connection")
		'''
		try and connect, if the process fails, exit and keep the program
		running.  this iwll allow for the client to be running while we wait for
		a camera to be connected 
		This will not handle a camera being disconnected during a connection.
		if we want that, have try include all of the "s" actions
		'''
		try:
			s.connect((host,port))
		except:
			print("connection error (%s,%s)"%(host,port))
			s.close()
			return("error")
			
		s.sendall(b'TI Pic please')	#ask for the data
		
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
		st1=('%s/%s/%s'%(f_dir,file,fname))	#file location
		cv2.imwrite(st1,decoded_image)	#write teh file
		print("File %s written"%st1)
		
		s.close()	#close the socket
	return fname
		

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
	f1=take_pic(HOST,PORT,b_file)
	f2=take_pic(Z_HOST,PORT,p_file)
	
	##this is where we'd insert the second camera
	##basically call this function twice, once for the zero, once for the pi
	

	
	#return the file name, we only use this for the website, and we're just going to return f1 since that's the easiest thing to do
	return f1

#if i'm the main dog, run this
if __name__=="__main__":
	directory_check()
	main_loop()
