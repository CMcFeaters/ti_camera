'''
This program is the server and runs on the picamera.  It is activeated when a request comes in.
This program:
-This program listens on a port.  
-When a request is received the program takes a picture and converts to an RGB stream
-Sends back to the client.

Server: PiCamera 192.168.1.247
Client: PiNAS 192.168.1.9

'''


from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from datetime import datetime as dt
import cv2
import socket
import numpy as np
import os
import math

HOST = "192.168.1.227"	#Pi_Camera address
PORT=65432	#non-privileged port

camera=PiCamera()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:	#AF_INET = AddressFamily Internet (IPV4), SOCK_STREAM = TCP
	s.bind((HOST,PORT))
	s.listen()	#bind and listen on the port we initiated
	
	while True:
		#Wait for a connection
		print("waiting")
		conn,add = s.accept()	#accept our connection and address of what we accepted, the program blocks on this line to a connection is received
		print("accepting from ",add)
		print("received: ",conn.recv(1024))
		
		#once a request has occured,
		#we take the picture
		print("Taking picture")
		camera.start_preview()
		sleep(2)
		rawdata=PiRGBArray(camera)	#RGB array object
		camera.capture(rawdata,'bgr')
		camera.stop_preview()
		
		#print some data
		print('Captured %dx%d image'%(rawdata.array.shape[1],rawdata.array.shape[0]))
		size=3*32*math.ceil(rawdata.array.shape[1]/32)*16*math.ceil(rawdata.array.shape[0]/16)
		kbs=math.ceil(size/1024)
		print('Image size: %d'%int(size))
		print('Number of kbs: %d'%int(kbs))
		
		#we process the image to be able to be sent
		image=rawdata.array
		encoded=cv2.imencode('.jpg',image)[1]
		
		with conn:
			#we respond back over the socket with the data
			print("replying with data")
			print(conn.sendall(encoded))
			print("Data sent")

		



