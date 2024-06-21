'''
image compare file
TRies to eliminate repeated images

will produce either the board images located in 'date'_B, the people images located in 'date'_P, or a synched set from both B and P files
the images are synched off of the board states.  This decision is based off of the command line option, b,p,s respectively.  Defaults to board

example usage:
	board
		python imgcmp.py
		python imgcmp.py b
	person
		python imgcmp.py p
	synch
		python imgcmp.py s
'''


from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp
import cv2
import os
import imageio
import sys
import bisect
import moviepy.editor as mp
from datetime import datetime as dt

game_date="20240531" #date you played the game/root of your P/B files

def get_time(file_name):
	'''
	given a file path, will return the datetime depicted by the file tag
	'''
	length=len(file_name)
	#print(file_name[length-19:length-4])
	t_value=file_name[length-19:length-4]
	return dt.strptime(t_value,"%Y%m%d_%H%M%S")

def key_func(t):
	print ("t0 %s - t1 %s"%(t[0],t[1]))
	return t[1]

def find_person(b_time,p_list):
	'''
	b_time:  the time associated with the board picture
	p_list: the list times of people pictures
	searches p_list for the closest time matching b_time
	returns that index
	'''
	
	index=bisect.bisect_left(p_list,b_time)	#find the index
	
	#verify the index is within the bounds, if it says it's the last item, just decrement by 1
	if index>=len(p_list):
		index=len(p_list)-1
	
	return index	#return the index 
	
	
def create_mp4s(t_path,g_date,path_dict,unique):
	'''
	t_path: the path to the location we are saving the files
	g_date: the name of the file, based off of the source file location
	path_dict: the dict containing the path locations
	unique: the list of unique file names
	starts by creating a gif by reading then appending all of the images
	the creates an MP4 from that gif
	'''
	print("creating %s Gif"%g_date)
	with imageio.get_writer(os.path.join(t_path,"TI_%s.gif"%g_date), mode='I') as writer:
		for filename in unique:
			image = imageio.imread(path_dict[filename])
			writer.append_data(image)
	print("Gif created, creating MP4")
	clip = mp.VideoFileClip("TI_%s.gif"%g_date)
	clip.write_videofile("TI_%s.mp4"%g_date)
	print("MP4 %s created"%g_date)
	
	

def main(g_files):
	#dicts for holding data
	path_dict={}	#a dictionary that contains all of the file paths
	key_dict={}		#a dictionary that contains a tuple of the file names (keys) and time values all of the keys of pathdict
	unique={}		#a dictionary used for tracking the unique picture
	
	#file paths
	s_paths=[os.path.abspath("Z:\\TI_%s"%g_date) for g_date in g_files]	#paths to the file locations, assumed to be mapped in our z:drive
	t_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\TI\\ti_camera")	#this is the folder where our files will be placed
	
	synch=len(g_files)>1	#helper variable to identify if we are doign a synch (creating multiple streams) or just a single picture source
	
	'''
	creates all of the dicts for use, can accomodate b, s, p
	each dict will have the B and P dates as keys, note "type" is also part of the path
	'''
	print ("Creating comparison list of game %s"%game_date)	
	for type in g_files:
		path_dict[type]={}	#create an empty dictionary under the "board/person" to store the file paths
		
		#populate the dict with the file paths
		for file in os.listdir(s_paths[g_files.index(type)]):
				path_dict[type][file]=os.path.join(s_paths[g_files.index(type)],file)	#create pathways to all the files taken during the game
				
		#create a sorted array of keys from this dict storing file nme and time
		key_dict[type]=[(key,get_time(key)) for key in path_dict[type].keys()]
		key_dict[type].sort()

		unique[type]=[] 	#create an array that holds all of the unique board picture file paths
	
	#begin comparison of images
	curr=0		#a basic counter
	
	'''
	this loop cycles through all of the sorted pictures.  It checks the current picture against the
	next picture.  If there is enough of a detla, it adds the current picture to the unique list 
	and then repeats that cycle by comparing that new picture against the next picture.  if there is not enough of a delta
	it skips the picture and moves on to the next.
	
	To account for the people pictures, the loop will still be driven by the board picture comparison, 
	when a unique board is found, it will try to find the accompanying people picture.  
	
	It will do this by trying to find the closest people timestamp from board timestamp. It uses the find_person, which does a bisect search.  To suppourt
	this searching, the person keylist tuples are split into two arrays, (p_files, p_times) p_times are sent to find_person so that they can be quickly used for bisect
	'''
	if synch:
		p_files,p_times=zip(*key_dict[g_files[1]])	#this splits the key dict into file names and times so we can use bisect during our find_person function
	
	for i in range(1,len(key_dict[g_files[0]])):
		x=key_dict[g_files[0]][curr][0]
		t1=cv2.imread(path_dict[g_files[0]][x])
		
		y=key_dict[g_files[0]][i][0]
		t2=cv2.imread(path_dict[g_files[0]][y])
		
		diff=mse(t1,t2)
		#print('{i:<7}: {x:<16} - {y:<16} : {a:<10.5f}'.format(i=i,x=x,y=y,a=diff))
		#found a difference picture
		if diff>100:
			unique[g_files[0]].append(key_dict[g_files[0]][curr][0])
			#this is lazy, but it's how we check to see if we are doing a person as well
			if synch:
				unique[g_files[1]].append(key_dict[g_files[1]][find_person(key_dict[g_files[0]][curr][1],p_times)][0])
			curr=i

	print("Done comparing")
	#append the last frame
	unique[g_files[0]].append(key_dict[g_files[0]][curr][0])	#add our last file
	
	#since we're only doign this once, we can just run the if statement and save our processing time
	if synch:
		unique[g_files[1]].append(key_dict[g_files[1]][find_person(key_dict[g_files[0]][curr][1],p_times)][0])
		#sometimes we have an off by 1 error if the board camera was turned off before the person camera and this will detect correct it
		while len(unique[g_files[1]])<len(unique[g_files[0]]):
			unique[g_files[1]].append(unique[g_files[1][len(unique[g_files[1]])-1]])
	
	
	
	#create_gif
	for type in g_files:
		create_mp4s(t_path,type,path_dict[type],unique[type])
	
if __name__=="__main__":
	
	if len(sys.argv)>0:
		#do board
		if sys.argv[1]=="b":
			g_files=["%s_B"%game_date]
		#do person
		elif sys.argv[1]=="p":
			g_files=["%s_P"%game_date]
		#do synch
		elif sys.argv[1]=="s":
			g_files=["%s_B"%game_date,"%s_P"%game_date]
	else:
		#default to board
		g_files=["%s_B"%game_date]
		
	main(g_files)
	