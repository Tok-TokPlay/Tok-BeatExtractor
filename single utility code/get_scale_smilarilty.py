import librosa
import matplotlib.pyplot as plt
import numpy as np

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
    for i in range(0, len(dest)) :
        temp.append(dest[i] * largest_sample / largest_dest)
    #MCC Code above.
    #Magnitude Control Compare.
    D, wp = librosa.dtw(sample, temp, subseq = True)
    return abs(D[-1,-1])

def get_scale_simmilarity(scale_set) :
    scale_list = []
    DTW_value = []
    for f in range(0, len(scale_set)) :
        for t in range(0, len(scale_set[f])) :
            scale_list.append(scale_set[f][t])
            DTW_value.append([])

    for i in range(0, len(scale_list)) :
        print("DTW_now... : " + str(i / len(scale_list) * 100) + "\t%")
        for j in range(0, len(scale_list)) :
            if j < i :
                DTW_value[i].append(DTW_value[j][i])
            else : 
                DTW_value[i].append(MCC_with_DTW(scale_list[i], scale_list[j]))    
    return DTW_value

max_len = 20

sample = []
for i in range(0, max_len) :
    sample.append([])

for i in range(0, max_len) :
    for j in range(0, max_len) :
        sample[i].append([])
        
for i in range(0, max_len) :
    for j in range(0, max_len) :
        for t in range(0, max_len) :
            sample[i][j].append((j % int(max_len/4) + 1) * np.sin((i+1) * np.pi + t))

DTW_value = get_scale_simmilarity(sample)

plt.figure()
plt.plot(DTW_value[0])
plt.show()
