import moviepy.editor as mp
import os
t_path=os.path.abspath("C:\\Users\\Chuck\\Documents\\Programs\\TI\\ti_camera")

clip = mp.VideoFileClip("TI_20240531_P.gif")
clip.write_videofile("TI_20240531_P.mp4")
