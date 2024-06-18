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
import moviepy.editor as mp
from datetime import datetime as dt

game_date="20240531" #date you played the game/root of your P/B files
index_offset=0	#this is used when trying to align the board and person indexes

def get_time(file_name):
	'''
	given a file path, will return the datetime depicted by the file tag
	'''
	length=len(file_name)
	t_value=file_name[length-19,length-4]
	return dt.strptime("%Y%m%d_%H%M%S")

def find_person(t_file,p_list,b_index):
	'''
	given a file name (t_file) this function will search through a list of people pictures (p_list) to find 
	a file that has a timestap within 5s of the t_file timestamp.  it will return that file path
	should start at b_index
	'''
	b_time=get_time(t_file)
	
	'''
	check the b_index against the index offset
	if b_index greater than offset p_index=b_index-offset,
	else there is no existing person to the board
	'''
	if b_index<index_offset:
		return "none"
	elif abs((get_time(t_file)-get_time(p_list[p_index])).total_seconds())<=10:
		return p_list[p_index]
	elif abs((get_time(t_file)-get_time(p_list[p_index+1])).total_seconds())<=10:
		return p_list[p_index+1]
	else:
		return "none"
		
	'''
	get p_time and compare against b_time, if timedelta.total_seconds()<10, it's a match
	p_file=p_list[p_index]
	if not, check the previous, if not, there is no equivalent
	p_file='none'
	'''
	
	
	

def main(g_files):
	#the following are dicts because we can now have 2 different sets of files, one for the board and one for the people
	path_dict={}	#a dictionary that contains all of the file paths
	key_dict={}		#a dictionary that contains all of the keys of pathdict
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
		path_dict[type]={}	#create an empty dictionary under the "board/person" to store the file paths
		for file in os.listdir(s_paths[0]):
			path_dict[type][file]=os.path.join(s_paths[0],file)	#this now contains a pathway to all the files taken during the game
		#create a sorted array of keys from this dict
		key_dict[type]=[key for key in path_dict[type].keys()]
		key_dict[type].sort()
		unique[type]=[] 	#an array that holds all of the unique board picture file paths
	
	#update index offset to different length pictures
	if len(key_dict)>1:
		index_offset=len(key_dict[g_files[0]])-len(key_dict[g_files[1]])
		if index_offset<0:
			index_offset=0
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
	for i in range(1,len(key_dict[g_files[0]])):
		x=key_dict[g_files[0]][curr]
		t1=cv2.imread(path_dict[x])
		
		y=key_dict[g_files[0]][i]
		t2=cv2.imread(path_dict[y])
		
		diff=mse(t1,t2)
		#print('{i:<7}: {x:<16} - {y:<16} : {a:<10.5f}'.format(i=i,x=x,y=y,a=diff))
		#found a difference picture
		if diff>100:
			unique[g_files[0]].append(key_dict[g_files[0]][curr])
			#this is lazy, but it's how we check to see if we are doing a person as well
			try:
				unique[g_files[1]].append(find_person(key_dict[g_files[0]][curr],key_dict[g_files[1]]))
			except:
				pass
			curr=i

	print("Done comparing")
	unique.append(key_dict[g_files[0]][curr])	#add our last file
	#for thing in unique:
	#	print(thing)

	print("Unique BOARD Pictures: %s"%len(unique[g_files[0]]))	
	print("Unique PEOPLE Pictures: %s"%len(unique[g_files[1]]))	
	#print(unique)
	#for thing in unique:
	#	print(path_dict[thing])
	
	#commenting this section out while testing
	'''
	print("creating Gif")
	#create_gif
	with imageio.get_writer(os.path.join(t_path,"TI_%s.gif"%g_date), mode='I') as writer:
		for filename in unique:
			image = imageio.imread(path_dict[filename])
			writer.append_data(image)
	print("Gif created, creating MP4")
	clip = mp.VideoFileClip("TI_%s.gif"%g_date)
	clip.write_videofile("TI_%s.mp4"%g_date)
	print("MP4 created")
	'''
if __name__=="__main__":
	
	if sys.argv[1]=="b":
		g_files=["%s_B"%game_date]
	elif sys.argv[1]=="p":
		g_files=["%s_P"%game_date]
	elif sys.argv[1]=="s":
		g_files=["%s_B"%game_date,"%s_P"%game_date]
		
	main(g_files)
	