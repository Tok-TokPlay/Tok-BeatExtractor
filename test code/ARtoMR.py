import wave
import struct
import math
import os
import numpy as np
import matplotlib.pyplot as plt

#D:/Workspace/Python/WAV
base = "D:/Workspace/Python/WAV_CUT"
f_song = "BornToBeNN_song3.wav"
f_inst = "BornToBeNN_inst3.wav"
f_vocal = "BornToBeNN_voca3.wav"
f_norm = "BornToBeNN_norm3.wav"

w_song = wave.open(os.path.join(base, f_song), "r")
w_inst = wave.open(os.path.join(base, f_inst), "r")
w_vocal = wave.open(os.path.join(base, f_vocal), "w")
w_normed = wave.open(os.path.join(base, f_norm), "w")

song_framerate = float(w_song.getframerate())
song_nframes = w_song.getnframes()

vocal_framerate = song_framerate
vocal_nframes = song_nframes
vocal_nchannels = w_song.getnchannels()
comptype = "NONE"
compname = "not compressed"
sampwidth = 2

Ts = 0.0001
Fs = 1/Ts

interval = 0.0625

time_var = np.arange(0.0, interval, Ts)
length = int(interval * song_framerate)
k = np.arange(length+1)
T = length/Fs
freq = k/T

normalization_value = 24

data = []

w_vocal.setparams((vocal_nchannels, sampwidth, vocal_framerate, vocal_nframes, comptype, compname))
w_normed.setparams((vocal_nchannels, sampwidth, vocal_framerate, vocal_nframes, comptype, compname))

if vocal_nchannels == 2 :
    for i in range(0, song_nframes) :
        if(i % 500 == 0) :
            print(i / song_nframes * 200)
        if(i > length * 200) :
            break
        song_data = w_song.readframes(1)
        inst_data = w_inst.readframes(1)
        vocal_data = ( struct.unpack("2h",song_data)[0] - struct.unpack("2h",inst_data)[0] 
,struct.unpack("2h",song_data)[1] - struct.unpack("2h",inst_data)[1] )
        if vocal_data[0] > -32769 and vocal_data[0] < 32768 :
            if vocal_data[1] > -32769 and vocal_data[1] < 32768 :
                w_vocal.writeframes(struct.pack('h', int(vocal_data[0])))
                w_vocal.writeframes(struct.pack('h', int(vocal_data[1])))
    print("Finished generating vocal========")
    w_vocal.close()
    w_vocal = wave.open(os.path.join(base, f_vocal), "r")
    ch1_dat = []
    ch2_dat = []
    deleted = 0
    for i in range(0, song_nframes) :
        if(i % 500 == 0) :
            print(i / song_nframes * 100)
        voc_data = w_vocal.readframes(1)
        ch1_dat.append(struct.unpack("2h",voc_data)[0] / length)
        ch2_dat.append(struct.unpack("2h",voc_data)[1] / length)
        if i % length == 0 and i != 0 :
            print("Started FFT============")
            end = int(i / length)
            Y1 = np.fft.fft(ch1_dat)
            Y2 = np.fft.fft(ch2_dat)
            print("Finished FFT============")
            for j in range(0, length - 1) :
                if abs(Y1)[j] < normalization_value :
                    Y1[j] =  Y1[j] / 256
                    deleted = deleted + 1
                elif abs(Y1)[j] < normalization_value * 2 :
                    Y1[j] =  Y1[j] / 64
                    deleted = deleted + 1
                if abs(Y2)[j] < normalization_value :
                    Y2[j] =  Y2[j] / 256
                    deleted = deleted + 1
                elif abs(Y2)[j] < normalization_value * 2 :
                    Y2[j] =  Y2[j] / 64
                    deleted = deleted + 1
            print("Started iFFT============")
            ch1_dat = np.fft.ifft(Y1)
            ch2_dat = np.fft.ifft(Y2)
            print("Finished iFFT============")
            print("Deleted : " + str(deleted) + " at " + str(length * 2))
            deleted = 0
            print("Started saving============")
            for j in range(0, length - 1) :
                if int(ch1_dat[j] * length) > 32767 or int(ch1_dat[j] * length) < -32768 :
                    w_normed.writeframes(struct.pack('h', 32760))
                else : 
                    w_normed.writeframes(struct.pack('h', int(ch1_dat[j] * length)))
                if int(ch2_dat[j] * length) > 32767 or int(ch2_dat[j] * length) < -32768 :
                    w_normed.writeframes(struct.pack('h', 32760))
                else : 
                    w_normed.writeframes(struct.pack('h', int(ch2_dat[j] * length)))
            print("Finished saving============")
            ch1_dat = []
            ch2_dat = []
                
else :
    for i in range(0, song_nframes) :
        if(i % 500 == 0) :
            print(i / song_nframes * 100)
        song_data = w_song.readframes(1)
        inst_data = w_inst.readframes(1)
        vocal_data = ( struct.unpack("2h",song_data)[0] - struct.unpack("2h",inst_data)[0])
        if vocal_data[0] > -32769 and vocal_data[0] < 32768 :
            w_vocal.writeframes(struct.pack('h', int(vocal_data[0])))

w_vocal.close()
w_norm.close()
w_song.close()
w_inst.close()
