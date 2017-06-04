'''
debugging console.
'''

import beat_cqt as bt
import beat_tie as bt2

dir_name = "/home/sshrik/Workspace/python/Tok-BeatExtractor/Others/Sample/v1.2/Sample060101"
file_name = "Sample 060101.wav"
#save_dir = "/home/sshrik/Workspace/python/Music/WAV"

bt.beatract(dir_name=dir_name,file_name=file_name, time_variation=0.05, \
debugmode=1 , show_graph=1, save_graph=1)