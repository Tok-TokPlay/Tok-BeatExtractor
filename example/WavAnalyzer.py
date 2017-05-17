# First, Open MIDI WAV file and see how frequency are distributed.
# Then, generate cosine wave file and saving it. Hearing what's different from origin file.
# It's good to know how harmonics are distributed.

# Second, erase around noise ( ex, 440hz + - 2.5 hz ) and hearing what is different.

import math
import wave
import numpy as np
import matplotlib.pyplot as plt

fileName = "WAV_ANALYS/GS_one_35.wav"
wav_file = wave.open(fileName, "r")


framerate = float(wav_file.getframerate()) # Wav file sound sampling frequency
nframes = wav_file.getnframes()

sampling_interval = 0.0625
framed_data_number = sampling_interval * framerate
time = np.arange(0, sampling_interval, 1 / framerate)

song_data = []
ch1_data = []
ch2_data = []
for i in range(0, nframes)  :
    waveData = wav_file.readframes(1)
    data.append(struct.unpack("<2h",waveData)
