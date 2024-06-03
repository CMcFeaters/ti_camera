'''
image compare file
TRies to eliminate repeated images
'''


from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp
import cv2
import os
import imageio
import sys
import moviepy.editor as mp


def main():
	testdict={}
	s_path=os.path.abspath("Z:\\TI_%s"%g_date)	#where are we getting the files from

	#test_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\ti_camera\\test_set")
	t_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\TI\\ti_camera")	#where are we writing the file

	filepaths=[os.path.join(s_path,file) for file in os.listdir(s_path)]	#generate file names
	filepaths.sort()

	#for thing in filepaths:
	#	print(thing)
	print ("Creating comparison list of game %s"%g_date)
	for file in os.listdir(s_path):#
		testdict[file]=os.path.join(s_path,file)

	temp=[key for key in testdict.keys()]
	temp.sort()
	curr=0
	unique=[]
	for i in range(1,len(temp)):
		
		x=temp[curr]
		t1=cv2.imread(testdict[x])
		y=temp[i]
		t2=cv2.imread(testdict[y])
		diff=mse(t1,t2)
		#print('{i:<7}: {x:<16} - {y:<16} : {a:<10.5f}'.format(i=i,x=x,y=y,a=diff))
		if diff>100:
			unique.append(temp[curr])
			curr=i
	print("Done comparing")
	unique.append(temp[curr])
	#for thing in unique:
	#	print(thing)

	print("Unique Picuters: %s"%len(unique))	
	#print(unique)
	#for thing in unique:
	#	print(testdict[thing])
	print("creating Gif")
	#create_gif
	with imageio.get_writer(os.path.join(t_path,"TI_%s.gif"%g_date), mode='I') as writer:
		for filename in unique:
			image = imageio.imread(testdict[filename])
			writer.append_data(image)
	print("Gif created, creating MP4")
	clip = mp.VideoFileClip("TI_%s.gif"%g_date)
	clip.write_videofile("TI_%s.mp4"%g_date)
	print("MP4 created")

if __name__=="__main__":
	if sys.argv[1]=="b":
		g_date="20240531_B"
	else if sys.argv[1]=="p":
		g_date="20240531_P"
		
	main()
	