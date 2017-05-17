import wave
import struct
import math
import numpy as np

f_song = "NNGNNO_song_p01.wav"
f_inst = "NNGNNO_inst_p01.wav"
f_vocal = "NNGNNO_voca_p01.wav"
f_my_vocal = "NNGNNO_my_voca_p01.wav"

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

ch1_data = []
ch2_data = []
for i in range(0, song_nframes) :
    if(i % 100 == 0) :
        print(i / song_nframes * 100)
    if i / song_nframes * 100 > 0.1 :
        break
    song_data = w_song.readframes(1)
    ch1_data.append(struct.unpack("2h",song_data)[0])
    ch2_data.append(struct.unpack("2h",song_data)[1])

fav = int(vocal_framerate / 10)
print(type(fav))

for i in range(0, song_nframes, (int)(vocal_framerate / 10)) : # 0.1 초 간격으로 fft 실행.
    if(i % 100 == 0) :
        print(i / song_nframes * 100)

    sp1 = np.fft.fft(ch1_data[i * fav: (i+1) * fav])
    sp2 = np.fft.fft(ch2_data[i * fav: (i+1) * fav])
    freq1 = np.fft.fftfreq(fav, 1 / vocal_framerate)
    freq2 = np.fft.fftfreq(fav, 1 / vocal_framerate)
    
    for j in range(i * fav, (i+1) * fav) :
        if freq1 > 80 and freq1 < 4000 and freq2 > 80 and freq2 < 4000 :
            w_vocal.writeframes(struct.pack('h', ch1_data[j]))
            w_vocal.writeframes(struct.pack('h', ch2_data[j]))

w_song.close()
w_inst.close()
w_vocal.close()
