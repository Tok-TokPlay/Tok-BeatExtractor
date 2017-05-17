import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


#========================== Part of loading=============================#
print("Now Loading file...")
y, sr = librosa.load("WAV_CUT/BornToBeNN_song3_per.wav", offset = 0.0, duration = 10)
#========================== Part of loading=============================#



'''
#========================== Part of STFT================================#
print("Now stft ...")
D = librosa.stft(y, center=False)
#========================== Part of STFT================================#
'''

'''
#========================== Part of Show================================#
print("Now Displaying ...")
librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
plt.title('Power Spectrogram.')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()
#========================== Part of Show================================#
'''

'''
#========================== Part of ISTFT===============================#
print("Now ISTFT...")
freq, D = librosa.ifgram(y,sr = sr)
for i in range(0, len(freq) - 1) :
    print(freq[i])
#========================== Part of ISTFT===============================#
'''


#========================== Part of CQT=================================#
C = librosa.cqt(y, sr=sr, fmin=librosa.note_to_hz('C1'), n_bins= 120, bins_per_octave= 12*2)
# n_bins / bins_per_octave ( 12 notes = 1 octave )
#========================== Part of CQT=================================#


#========================== Part of Show================================#
librosa.display.specshow(librosa.amplitude_to_db(C, ref=np.max), sr=sr, x_axis='time', y_axis='cqt_note')
plt.colorbar(format='%+2.0f dB')
plt.title('CQT power spectrum')
plt.tight_layout()
plt.show()
#========================== Part of Show================================#
