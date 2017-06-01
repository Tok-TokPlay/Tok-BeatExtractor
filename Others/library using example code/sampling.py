import wave
import struct
import sys

import numpy as np

fname = ".\GHeyKid_inst.WAV"
fname = "GHeyKid_inst_sample.wav"
wav_file = wave.open(fname, "r")

framerate = float(wav_file.getframerate())
nframes = wav_file.getnframes()

print(framerate)
print(nframes)
time = np.arange(0, nframes/framerate, 1/framerate)
data = []
for i in range(0,nframes):
    waveData = wav_file.readframes(1)
    if i % 100 == 0 :
        print(i/nframes * 100)
    if i / nframes *100 > 1 :
        break;
    data.append(struct.unpack("bh",waveData))

wav_file.close()


freq = 1000.0
data_size = 40000*4
fname = "WaveTest.wav"
frate = 44100.0
amp = 64000.0     # multiplier for amplitude
     
wav_file = wave.open(fname, "w")

nchannels = 1
sampwidth = 2
framerate = int(frate)
nframes = data_size
comptype = "NONE"
compname = "not compressed"

wav_file.setparams((nchannels, sampwidth, framerate, nframes,
    comptype, compname))

for s in sine_list_x:
    # write the audio frames to file
    wav_file.writeframes(struct.pack('h', int(s * amp/2)))



wav_file.close()
