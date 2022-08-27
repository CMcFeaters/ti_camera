import imageio
import os

s_path=os.path.abspath("Z:\\TI_20220812")	#where are we getting the files from
t_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\ti_camera")	#where are we writing the file

filenames=[os.path.join(s_path,file) for file in os.listdir(s_path)]	#generate file names
filenames.sort()
with imageio.get_writer(os.path.join(t_path,"TI.gif"), mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)