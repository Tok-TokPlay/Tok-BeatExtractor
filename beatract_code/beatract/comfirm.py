'''
debugging console.
'''

import beat_cqt as bt
import beat_tie as bt2

dir_name = "/home/sshrik/Workspace/python/Regacy of void/WAV_CUT"
file_name = "BornToBeNN_inst4.wav"
#save_dir = "/home/sshrik/Workspace/python/Music/WAV"

bt.beatract(dir_name=dir_name, time_variation=0.05, \
debugmode=1, save_graph=1)