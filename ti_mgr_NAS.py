#!/home/pi/tienv/bin/python3
'''
python 3.8
redis
cv2

'''

'''
This program manages the TI_portion of the PI_Camera client.  It:
-auto_starts with the pi
-has error catching
-provides it's status when requested
-provides the status of the client_ti_cam
-starts the ti cam if not running
-gets the client_ti_cam status

-must use redis PIDs for this one

'''
from time import sleep
import sys
import redis
import socket
import psutil	#to query process IDs

HOST="127.0.0.1"	#hang out on local host
PORT="54321"		#hang out on local host

r = redis.Redis(host='localhost', port=6379, db=0)	#redis entry

def main_loop():
	"""
	
	"""
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		conn,add =s.accept()
		request=conn.recv(1024).decode("utf-8")
		print("accepting from: ",add)
		print("received: ",request)
		
		if request=="client_status":
			conn.sendall(get_client_status())
		else conn.sendall(b"message received: %s please use the following:\nclient_status - get client status"%request)	

	
def get_client_status():
	"""
		gets the status of the client_ti_cam process
		reads the "client_cam" redis entry to determine the pid for the process
		checks the pid to determine if it's running
	"""
	pid=r.get("client_cam").decode("utf-8")
	if psutil.Process(pid)=="running":
		return "running"
	else:
		return "fault"


if __name__=="__main__":
	main_loop()

