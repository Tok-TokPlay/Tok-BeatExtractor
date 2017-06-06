'''
debugging console.
'''

import beat_cqt as bt
import beat_tie as bt2

dir_name = "/home/sshrik/Workspace/python/Regacy of void/MP3"
file_name = "STK10CM_song.mp3"
#save_dir = "/home/sshrik/Workspace/python/Music/WAV"

bt.beatract(dir_name=dir_name, file_name=file_name, time_variation=0.05, \
debugmode=1, save_graph=1, addable_option="-y ")