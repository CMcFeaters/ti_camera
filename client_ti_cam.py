'''
This program is the client runs on the NAS.  It is activated by the client php when a user opens the page.
This program:
-Send a request to the PIcam to take a pic
-Receives that data from picam
-WRites the data to a file
-prints the name of the file for use by the php file

Server: PiCamera 192.168.1.227
Client: PiNAS 192.168.1.9

'''

#from picamera.array import PiRGBArray
#from picamera import PiCamera
from time import sleep
from datetime import datetime as dt
import cv2
import socket
import numpy as np
import os

HOST = "192.168.1.227"	#basic loopback for local host
PORT=65432	#non-privileged port


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	
	#ask for a picture from the server
	print("Data request recieved by user, initiating connection")
	s.connect((HOST,PORT))
	s.sendall(b'Doodle Pic please')
	
	#once we connect, recieve the response
	#receive until connection is closed
	data=0
	data=s.recv(1024)	#our buffer is 1024 bytes
	i=0
	while 1:
		print('Receiving %d'%i)
		tdata=s.recv(1024)
		if not tdata: break
		data+=tdata
		i+=1
	print("File %d received"%i)
	
	#Write the file
	encoded_array=np.fromstring(data,np.uint8)	#convert from string to array
	decoded_image=cv2.imdecode(encoded_array,cv2.IMREAD_COLOR)	#decode arryay to image
	fname='%s_doodle.jpg'%dt.now().strftime("%Y%m%d_%H%M%S")
	st1=('/mnt/raid1/shared/doodle/%s'%fname)	#file location
	cv2.imwrite(st1,decoded_image)	#write teh file
	print("File %s written"%st1)
	
	#print the name of the file
	print(fname)
	s.close()		