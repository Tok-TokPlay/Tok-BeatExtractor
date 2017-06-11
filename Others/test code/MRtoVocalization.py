import wave
import struct

def vocalization(mp3_file, mr_file, save_dir=-1, mp3_dir=-1, mr_dir=-1, ar_name=-1):

# Control part
mp3_dir_flag = False
mr_dir_flag = False
save_dir_falg = False
ar_flag = False

if save_dir != -1:
	# Save to save_dir. if not, Save to mr directory.
	save_dir_falg = True

if mp3_dir != -1:
	# find at mp3_dir. if not, find to same python folder.
	mp3_dir_flag = True

if mr_dir != -1:
	# find at mp3_dir. if not, find to same python folder.
	mr_dir_flag = True

if ar_name != -1:
	# saving file name. if not, save with mp3_file(AR).mp3 or wav.
	ar_flag = True

if mp3_dir_flag:
	mp3_file_name = mp3_dir + "/" + mp3_file

if mr_dir_flag:
	mr_file_name = mr_dir + "/" + mr_file

# save file name to f_song and f_inst.
f_song = mp3_file_name
f_inst = mr_file_name

if ar_flag:
	if save_dir_flag:
		ar_file = save_dir + "/" + ar_name
	else:
		ar_file = ar_name
else:
	# Initialize ar_file name with "".
	ar_file = ""
	
	# For all split name with "." in file name...
	for string_number in range(0, len(mp3_file_name.split(".") - 1)):
		# Get all except like ".mp3".
		ar_file += mp3_file_name.split(".")[string_number]

	ar_file += "(AR)" + mp3_file_name.split(".")[-1]

# save file name ( ar_file ) to f_vocal.
f_vocal = ar_file

w_song = wave.open(f_song, "r")
w_inst = wave.open(f_inst, "r")
w_vocal = wave.open(f_vocal, "w")

song_framerate = float(w_song.getframerate())
song_nframes = w_song.getnframes()

vocal_framerate = song_framerate
vocal_nframes = song_nframes
vocal_nchannels = w_song.getnchannels()
comptype = "NONE"
compname = "not compressed"
sampwidth = 2

# Set wav file parameter.
w_vocal.setparams((vocal_nchannels, sampwidth, vocal_framerate, vocal_nframes, comptype, compname))

if vocal_nchannels == 2:
	# If channer is 2...
	for i in range(0, song_nframes) :
		# for all range of songs, add euclidean distance with 2 song.
		song_data = w_song.readframes(1)
		inst_data = w_inst.readframes(1)
		vocal_data = ( struct.unpack("2h",song_data)[0] - struct.unpack("2h",inst_data)[0] ,struct.unpack("2h",song_data)[1] - struct.unpack("2h",inst_data)[1] )
		# if distance is in range of below...
		if vocal_data[0] > -32769 and vocal_data[0] < 32768 :
		    if vocal_data[1] > -32769 and vocal_data[1] < 32768 :
		        w_vocal.writeframes(struct.pack('h', int(vocal_data[0])))
		        w_vocal.writeframes(struct.pack('h', int(vocal_data[1])))

# Close used files.
w_song.close()
w_inst.close()
w_vocal.close()
