'''
image compare file
TRies to eliminate repeated images

will produce either the board images located in 'date'_B, the people images located in 'date'_P, or a synched set from both B and P files
the images are synched off of the board states.  This decision is based off of the command line option, B, P, or S respectively.
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
index_offset=0	#this is used when trying to align the board and person indexes

'''
	#we should rewrite this so we just get the offset, find the time that matches closest and then grab pictures simultaneously
	#this can assume we are always taking a board pic then a people pic
	Basic strategy:
		1) find the offset in time
		2) use the offset to find the closest time matchup
		3) 
'''

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
	given a file name (t_file) this function will search through a list of people pictures (p_list) to find 
	a file that has a timestap within 5s of the t_file timestamp.  it will return that file path
	should start at b_index
	'''
	#b_time=get_time(t_file)
	#print ("Search time:  %s"%b_time)
	
	'''
	check the b_index against the index offset
	if b_index greater than offset p_index=b_index-offset,
	else there is no existing person to the board
	'''
	'''print("matching %s comparing against %s and %s"%(b_time,get_time(p_list[b_index]),get_time(p_list[b_index+1])))
	if b_index<index_offset:
		print("Index error")
		#print ("%s is < %s"%(b_index,index_offset))
		return "none"
	elif abs((get_time(t_file)-get_time(p_list[b_index])).total_seconds())<=10:
		print(p_list[b_index])
		return p_list[b_index]
	elif abs((get_time(t_file)-get_time(p_list[b_index+1])).total_seconds())<=10:
		print(p_list[b_index+1])
		return p_list[b_index+1]
	else:
		print ("None Found")
		print(abs((get_time(t_file)-get_time(p_list[b_index])).total_seconds()))
		print(abs((get_time(t_file)-get_time(p_list[b_index+1])).total_seconds()))
		return "none"
	'''
	index=bisect.bisect_left(p_list,b_time)
	'''try:
		print("Btime %s\nPtime %s (closest)\nIndex %s"%(b_time,p_list[index],index))
	except:
		print("len %s index %s"%(len(p_list),index))
	'''
	if index>=len(p_list):
		index=len(p_list)-1
	#print("len %s index %s"%(len(p_list),index))
	'''for p_file in p_list:
		#sorted list
		#negative number: board time is less than person and we can still approach by incrementing person
		#positive number: board time is more than person and we cannot approach by incrementing
		t_delta=(b_time-p_file[1]).total_seconds()
		print("%s - %s = %s"%(b_time,p_file[1],t_delta))
	'''	
	return index
	
	'''
	get p_time and compare against b_time, if timedelta.total_seconds()<10, it's a match
	p_file=p_list[p_index]
	if not, check the previous, if not, there is no equivalent
	p_file='none'
	'''
	
def create_mp4s(t_path,g_date,path_dict,unique):
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
	#the following are dicts because we can now have 2 different sets of files, one for the board and one for the people
	path_dict={}	#a dictionary that contains all of the file paths
	key_dict={}		#a dictionary that contains a tuple of the file names (keys) and time values all of the keys of pathdict
	unique={}		#a dictionary used for tracking the unique picture
	
	s_paths=[os.path.abspath("Z:\\TI_%s"%g_date) for g_date in g_files]	#paths to the file locations, assumed to be mapped in our z:drive

	#test_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\ti_camera\\test_set")
	t_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\TI\\ti_camera")	#this is the folder where our files will be placed
	
	#NOTE: WE MAY NO LONGER USE THIS
	#filepaths=[[os.path.join(s_path,file) for file in os.listdir(s_path)] for s_path in s_paths]	#this is the list of filenames in each folder, in the form of [B,P]
	#[thing.sort() for thing in filepaths]	#sorts the list of files in each path so we can compare them sequentially
	

	#for thing in filepaths:
	#	print(thing)
	#this section creates the dict of file paths to look at for comparison
	#it will have to create two of these, just like filepath
	print ("Creating comparison list of game %s"%game_date)
	
	for type in g_files:
		print(type)
		i=0	#temp counter for testing
		path_dict[type]={}	#create an empty dictionary under the "board/person" to store the file paths
		for file in os.listdir(s_paths[g_files.index(type)]):
				path_dict[type][file]=os.path.join(s_paths[g_files.index(type)],file)	#this now contains a pathway to all the files taken during the game
		#create a sorted array of keys from this dict
		key_dict[type]=[(key,get_time(key)) for key in path_dict[type].keys()]
		key_dict[type].sort()
		#print(key_dict[type])
		
		unique[type]=[] 	#an array that holds all of the unique board picture file paths
	
	#update index offset to different length pictures
	#i think this should be a time offset, aka, what's the time delta between these items
	#get each groups start time, if board starts before 
	
	if len(key_dict)>1:
		index_offset=len(key_dict[g_files[0]])-len(key_dict[g_files[1]])
		if index_offset<0:
			index_offset=0
	print("offset: %s"%index_offset)
	

	#begin comparison of images
	curr=0		#a basic counter
	
	print(g_files)
	

	'''
	this loop cycles through all of the sorted pictures.  It checks the current picture against the
	next picture.  If there is enough of a detla, it adds the current picture to the unique list 
	and then compares the new picture against the next picture.  if there is not enough of a delta
	it skips the picture and moves on to the next.
	
	To account for the people pictures, the loop will still be driven by the board picture comparison, 
	when a unique board is found, it will try to find the accompanying people picture.  
	
	It will do this by trying to find the closest increasing timestamp from its timestamp (pictures are
	taken in the order of board then people).  If it can't find one within 5s, it will just add "none"
	'''
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
			#try:
			unique[g_files[1]].append(key_dict[g_files[1]][find_person(key_dict[g_files[0]][curr][1],p_times)][0])
			#except:
			#pass
			curr=i

	print("Done comparing")
	#append the last frame
	unique[g_files[0]].append(key_dict[g_files[0]][curr][0])	#add our last file
	
	#since we're only doign this once, we can just run the if statement and save our processing time
	if len(g_files)>1:
		unique[g_files[1]].append(key_dict[g_files[1]][find_person(key_dict[g_files[0]][curr][1],p_times)][0])
		#sometimes we have an off by 1 error if the board camera was turned off before the person camera and this will detect correct it
		while len(unique[g_files[1]])<len(unique[g_files[0]]):
			unique[g_files[1]].append(unique[g_files[1][len(unique[g_files[1]])-1]])
	
	
	print("Unique BOARD Pictures: %s"%len(unique[g_files[0]]))	
	print("Unique PEOPLE Pictures: %s"%len(unique[g_files[1]]))	
	#print(unique)
	#for thing in unique:
	#	print(path_dict[thing])
	
	#commenting this section out while testing
	
	
	#create_gif
	for type in g_files:
		create_mp4s(t_path,type,path_dict[type],unique[type])
	
if __name__=="__main__":
	
	if sys.argv[1]=="b":
		g_files=["%s_B"%game_date]
	elif sys.argv[1]=="p":
		g_files=["%s_P"%game_date]
	elif sys.argv[1]=="s":
		g_files=["%s_B"%game_date,"%s_P"%game_date]
		
	main(g_files)
	