import os
import sys
import subprocess

dir_name = "/home/sshrik/Workspace/python/Music/MP3"

if len(sys.argv) == 1 :
	# if there doesn't exist command parameter...
	dir_name = "/home/sshrik/Workspace/python/Music/MP3"	
else :
	# if there exist comman parameter...
	dir_name = sys.argv[1]

filenames = os.listdir(dir_name)

for filename in filenames :
	# add full_name dir_name.
	# actually full_name is full path of file name.
	full_name = dir_name + "/"  + filename	
	#wav_name is wav file name.
	wav_name = "/home/sshrik/Workspace/python/Music/WAV"
	print("File chaging... " + full_name + " to " + wav_name)
	
	os.system('ffmpeg -i ' + '\'' + full_name + '\'' + '\'' + wav_name + '\'')
