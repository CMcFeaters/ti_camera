This repo contains code for client server camera setup.  There are two camera servers that take and send pictures to the client via sockets.  The client is a NAS which stores the data. 

This code also contains an image creater which analyze and convert all of the images into synchronized (if selected) MP4s.

client needs
-redis
-apache
-"aim mode"
-non-blocking socket requests e.g., fault handling if a camera is unplugged
client python libraries
-cv2
-redis
