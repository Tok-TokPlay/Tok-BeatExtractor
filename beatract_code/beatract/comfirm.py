'''
debugging console.
'''

import beat_cqt as bt
import beat_tie as bt2

dir_name = "/home/sshrik/Music/Dest"
#save_dir = "/home/sshrik/Workspace/python/Music/WAV"

bt.beatract(dir_name=dir_name, time_variation=0.05, \
debugmode=1, save_graph=1, addable_option="-y ")