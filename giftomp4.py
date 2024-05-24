import moviepy.editor as mp
import os
t_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\TI\\ti_camera")

clip = mp.VideoFileClip("TI_20230310.gif")
clip.write_videofile("TI_20230310.mp4")
