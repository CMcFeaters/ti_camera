"""
Program to auto scp files to/from designated pi and computer to aid in development
reads a config file "SCP.config" and present the user with a set of options to execute
config file is in the format
[source filename],[destination filename]
users execute the program "python auto_scp X" where X is the row number to be executed.
"""
from paramiko import SSHClient
from scp import SCPClient
import sys

PI_NAS='192.168.1.9'

def setup_copy(choice):
	'''
	loads the dict of selected files
	SCPs the users choice to the PI-NAS
	'''
	choice=int(choice)
	fdict=load_config()
	auto_copy(fdict[choice][0],fdict[choice][1])
	
	
def load_config():
	'''
	loads the config rile, returns a dict in the form of {('1',(file,file))}
	'''
	f=open("scp_config.txt","r")
	i=0
	fdict={}
	lines=f.readlines()
	for line in lines:
		files=line.split(',')
		if len(files)>1:
			fdict[i]=(files[0],files[1])
		i+=1
	return fdict

def auto_copy(source,dest):
	'''
	Takes in the source and destination filenames as inputs (including locations if not ./
	opens ssh
	opens scp using keys
	writes to dest (pi)
	'''
	
	with SSHClient() as ssh:
		ssh.load_system_host_keys()
		ssh.connect(PI_NAS,username='pi')
		with SCPClient(ssh.get_transport()) as scp:
			scp.put(source, remote_path=source)
	print ("Transfered file: %s"%source)
	print ("To: %s: %s"%(PI_NAS,source))

if __name__=="__main__":
	if len(sys.argv)>1:
		setup_copy(sys.argv[1])
	else:
		print("Please select an option:")
		dict=load_config()
		for thing in dict.keys():
			print(thing,dict[thing][0])