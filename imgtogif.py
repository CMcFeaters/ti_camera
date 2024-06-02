import imageio
import moviepy.editor as mp
import os
import sys

def main():
	s_path=os.path.abspath("Z:\\TI_%s"%g_date)	#where are we getting the files from
	t_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\TI\\ti_camera")	#where are we writing the file

	filenames=[os.path.join(s_path,file) for file in os.listdir(s_path)]	#generate file names
	filenames.sort()
	with imageio.get_writer(os.path.join(t_path,"%s.gif"%g_date), mode='I') as writer:
		for filename in filenames:
			image = imageio.imread(filename)
			writer.append_data(image)
			
	clip = mp.VideoFileClip("%s.gif"%g_date)
	clip.write_videofile("%s.mp4"%g_date)
		
if __name__=="__main__":
	if sys.argv[1]=="b":
		g_date="20240531_B"
	else:
		g_date="20240531_P"
		
	main()