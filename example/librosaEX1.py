import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

print("Now Loading file...")
y, sr = librosa.load("WAV_CUT/AMPM_song2.wav", offset=0.0, duration = 10.0)

'''
# Click Example ( for what is click )
print("Now finding beat...")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
y_beats = librosa.clicks(frames=beats, sr=sr)

print("Now making click...")
y_beats = librosa.clicks(frames=beats, sr=sr)
# length=len(y) Option will generate a signal of same length of y

times = librosa.frames_to_time(beats, sr=sr)
y_beat_times = librosa.clicks(times=times, sr=sr)
# Use timing instead of frame indices.

print("Now making plot...")
plt.figure()
S = librosa.feature.melspectrogram(y=y, sr=sr)
ax = plt.subplot(2, 1, 2)
librosa.display.specshow(librosa.power_to_db(S, ref=np.max), x_axis='time', y_axis='mel')
plt.subplot(2,1,1, sharex=ax)
librosa.display.waveplot(y_beat_times, sr=sr, label='Beat clicks')
plt.legend()
plt.xlim(15, 30)
plt.tight_layout()
plt.show()

'''

# Beat Example
print("Now Beat Tracking...")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
temp = librosa.beat.tempo(librosa.onset.onset_strength(y, sr=sr), sr=sr, aggregate=None)
beat_time = librosa.frames_to_time(beats, sr=sr)
print(temp)
for i in range(0, len(beat_time) - 2) :
    print(beat_time[i+1] - beat_time[i])


'''
# Auto Co-relation
print("Now Auto-correlationing...")
odf = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
# Onset Analyzing.
n = 4
ac = librosa.autocorrelate(odf, max_size=n* sr / 512)
# Fine auto-correlation in n Seconds
print("Now Plotting...")
plt.plot(ac)
plt.title('Auto Correlation')
plt.xlabel('Lag(frames)')
plt.show()
'''


# Onset Dectection
print("Now Dectecting Onset..")
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
# Search y.wav, sr : sampling rate
o_env = librosa.onset.onset_strength(y, sr=sr)
times = librosa.frames_to_time(np.arange(len(o_env)), sr=sr)
onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

D = librosa.stft(y)
plt.figure()

ax1 = plt.subplot(2, 1, 1)
librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), x_axis='time', y_axis='log')
plt.title('Power Spectrogram')
plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(times, o_env, label='Onset Strength')
plt.vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.9, linestyle='--', label='Onsets')
plt.axis('tight')
plt.legend(frameon=True, framealpha=0.75)
plt.show()

