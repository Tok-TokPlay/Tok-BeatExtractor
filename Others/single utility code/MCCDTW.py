import numpy as np
import librosa

def MCC_with_DTW(sample, dest) :
    largest_sample = 0
    for i in range(0, len(sample)) :
        if largest_sample < sample[i] :
            largest_sample = sample[i]

    largest_dest = 0
    for i in range(0, len(dest)) :
        if largest_dest < dest[i] :
            largest_dest = dest[i]
    temp = []
    print(largest_sample / largest_dest)
    for i in range(0, len(dest)) :
        temp.append(dest[i] * largest_sample / largest_dest)
    #MCC Code above.
    #Magnitude Control Compare.
    print("Start Calc DTW.")
    D, wp = librosa.dtw(sample, temp, subseq = True)
    return D, wp


sample = []
for i in range(0, 1000) :
    sample.append(np.sin(np.pi/16 * i))

dest = []
for i in range(0, 2000) :
    if i >= 500 and i < 1500 :
        dest.append(2 / 3 * np.sin(np.pi / 16 * (i-500)))
    else :
        dest.append(0)

print("Start Calc mcc with dtw.")
D, wp = MCC_with_DTW(sample, dest)
print(wp)
print(D[-1, -1])
print(D)
