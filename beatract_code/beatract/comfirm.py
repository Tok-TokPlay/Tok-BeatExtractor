'''
debugging console.
'''

import beat_cqt as bt
import beat_tie as bt2


'''
dir_name = "/home/sshrik/Music/2100 + 0709"
#save_dir = "/home/sshrik/Workspace/python/Music/WAV"

bt.beatract(dir_name=dir_name, time_variation=0.05, \
debugmode=1, save_graph=1, addable_option="-y ")
'''

save_dir = "/home/sshrik/Music/MR_MP3"
mr_dir = "/home/sshrik/Music/MR_MP3"
mp3_dir = "/home/sshrik/Music/MR_MP3"
mp3_name = "ManySnowWater.mp3"
mr_name = "ManySnowWater(inst).mp3"

bt.vocalization(mp3_file=mp3_name, mr_file=mr_name, save_dir=save_dir, mp3_dir=mp3_dir, mr_dir=mr_dir, ar_name=-1)