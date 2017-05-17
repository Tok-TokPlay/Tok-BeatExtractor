import librosa
import librosa.display

print("Now Loading file...")
s_n = "WAV_CUT/BornToBeNN_song3.wav"
y, sr = librosa.load(s_n)

print("Now Dividing file...")
y_h, y_p = librosa.effects.hpss(y)
print("Now Pitching file...")
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

s_h = "WAV_CUT/BornToBeNN_song3_har.wav"
s_p = "WAV_CUT/BornToBeNN_song3_per.wav"


print("Now Saving file...")
librosa.output.write_wav(s_h, y_h, sr);
librosa.output.write_wav(s_p, y_p, sr);

print(len(pitches))


for j in range(0, len(pitches[0])-1) :
    for i in range(0, len(pitches)-1) :
        if magnitudes[i,j] != 0 :
            print("At " + str(0.3 * j) + " ~ " +  str(0.3 * ( j + 1 )) + " Seconds.")
            print("Hz : " + str(pitches[i, j]) + "\tdB : " + str(magnitudes[i, j]))
#pitches[f, t]      magnitudes[f, t]
#f : Frequency num  Frequency large    
#t : at time t      at time t

