import wave
import struct
import math
import numpy as np

f_song = "NNGNNO_song.wav"
f_inst = "NNGNNO_inst.wav"
f_vocal = "NNGNNO_voca.wav"
f_my_vocal = "NNGNNO_my_voca.wav"

w_song = wave.open(f_song, "r")
w_inst = wave.open(f_inst, "r")
w_vocal = wave.open(f_vocal, "w")
w_my_vocal = wave.open(f_my_vocal, "w")

song_framerate = float(w_song.getframerate())
song_nframes = w_song.getnframes()

vocal_framerate = song_framerate
vocal_nframes = song_nframes
vocal_nchannels = w_song.getnchannels()
comptype = "NONE"
compname = "not compressed"
sampwidth = 2

data = []
my_data = []

w_vocal.setparams((vocal_nchannels, sampwidth, vocal_framerate, vocal_nframes, comptype, compname))
w_my_vocal.setparams((vocal_nchannels, sampwidth, vocal_framerate, vocal_nframes, comptype, compname))

for i in range(0, song_nframes) :
    if(i % 100 == 0) :
        print(i / song_nframes * 100)
    song_data = w_song.readframes(1)
    inst_data = w_inst.readframes(1)
    vocal_data = ( struct.unpack("2h",song_data)[0] - struct.unpack("2h",inst_data)[0] ,struct.unpack("2h",song_data)[1] - struct.unpack("2h",inst_data)[1] )
    if vocal_data[0] > -32769 :
        if vocal_data[0] < 32768 :
            if vocal_data[1] > -32769 :
                if vocal_data[1] < 32768 :
                    w_vocal.writeframes(struct.pack('h', int(vocal_data[0])))
                    w_vocal.writeframes(struct.pack('h', int(vocal_data[1])))
w_song.close()
w_inst.close()
w_vocal.close()
