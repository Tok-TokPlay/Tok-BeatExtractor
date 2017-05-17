import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def MCC_with_DTW(sample, dest) :
    largest_sample = 0.0000000001
    for i in range(0, len(sample)) :
        if largest_sample < sample[i] :
            largest_sample = sample[i]

    largest_dest = 0.0000000001
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

def take_local_maximum(CQT_result, threshold) :
    high = []
    result = []
    for t in range(0, len(CQT_result[0])) :
        for i in range(0, len(CQT_result)) :
            if CQT_result[i][t] > threshold :
                # i th scale at time t is larger then threshold...
                high.append(i)
        result.append(high)
        high = []
    return result

    
def max_len(freq_index) :
    maximum = 0
    for i in range(0, len(freq_index)):
        if len(freq_index[i]) > maximum :
            maximum = len(freq_index[i])
    return maximum

def parse_noise(CQT_result, MAG_threshold) :
    CQT_noise = []
    CQT_harmonic = []
    for f in range(0, len(CQT_result)) :
        CQT_noise.append([])
        CQT_harmonic.append([])

    for f in range(0, len(CQT_result)):
        for t in range(0, len(CQT_result[0])):
            if abs(CQT_result[f][t]) > MAG_threshold :
                CQT_harmonic[f].append(CQT_result[f][t])
                CQT_noise[f].append(0)
            else :
                CQT_harmonic[f].append(0)
                CQT_noise[f].append(CQT_result[f][t])

    return CQT_noise, CQT_harmonic

def get_threshold(CQT_result, seed = 0.95, result_hop = 1000) :
    '''
    This method or function return the threshold number for CQT_result.
    '''
    result_list = []
    for f in range(0, len(CQT_result)) :
        for t in range(0, len(CQT_result[0])) :
            result_list.append(abs(CQT_result[f][t]))
    result_list.sort()
    
    sorted_tangent = []
    for i in range(0, len(result_list) - result_hop) :
        sorted_tangent.append((result_list[i + result_hop] - result_list[i]))
        
    maximum_tangent = 0
    maximum_index = -1
    
    for i in range(0, len(sorted_tangent)) :
        if maximum_tangent < sorted_tangent[i] :
            maximum_tangent = sorted_tangent[i]
            maxumum_index = i
            
    small_tangent_index = -1
    large_tangent_index = -1
    
    for i in range(0, len(sorted_tangent)) :
        if small_tangent_index == -1 :
            if sorted_tangent[i] > (1 - seed) * maximum_tangent / 2 :
                small_tangent_index = i
        if large_tangent_index == -1 :
            if sorted_tangent[i] < (seed) * maximum_tangent / 2 :
                large_tangent_index = i

    return result_list[small_tangent_index], result_list[large_tangent_index]

def get_scale(CQT_harmonic) :
    time_set = []
    scale_set = []

    for f in range(0, len(CQT_harmonic)) :
        scale_set.append([])
        time_set.append([])

    recording = False
    st = 0
    ft = 0
    temp = []
    for f in range(0, len(CQT_harmonic)) :
        for t in range(0, len(CQT_harmonic[0])) :
            if recording == True :
                if abs(CQT_harmonic[f][t]) == 0 :
                    ft = t - 1
                    scale_set[f].append(temp)
                    time_set[f].append([st,ft])
                    recording = False
                    temp = []
                else :
                    temp.append(CQT_harmonic[f][t])
            else :
                if abs(CQT_harmonic[f][t]) != 0 :
                    st = t
                    recording = True
                    temp.append(CQT_harmonic[f][t])
    return scale_set, time_set

def get_ith_DRW(scale_set, DTW_value, freq) :
    ith_list = []
    start = 0
    end = 0
    
    for i in range(0, freq) :
        start = start + len(scale_set[i])
    end = start + len(scale_set[freq])

    for f in range(start, end) :
        ith_list.append(DTW_value[i])

    return ith_list
    

def collect_with_DTW(DTW_value, time_set,threshold) :
    for f in range(0, len(time_set)) :
        for i in range(0, len(time_set[f])) :
            print()

def get_scale_simmilarity(scale_set) :
    scale_list = []
    DTW_value = []
    for f in range(0, len(scale_set)) :
        for t in range(0, len(scale_set[f])) :
            scale_list.append(scale_set[f][t])
            DTW_value.append([])
    print(len(scale_list))
    for i in range(0, len(scale_list)) :
        print("DTW_now... : " + str(i / len(scale_list) * 100) + "\t%")
        for j in range(0, len(scale_list)) :
            if j < i :
                DTW_value[i].append(DTW_value[j][i])
            else : 
                DTW_value[i].append(MCC_with_DTW(scale_list[i], scale_list[j]))    
    return DTW_value
    

def converge_audio(scale_set, time_set, song_length) :
    audio_list = make_empty_list(1, len(time_set), song_length)
    time_setN = make_empty_list(1, len(time_set))
    
    print("Starting Initializing.")
    
    finished_freq = 0
    time = 0
    for i in range(0, len(audio_list)) :
        for j in range(0, len(audio_list[i])) :
            audio_list[i][j] = 0
            
    for i in range(0, len(time_set)) :
        time_setN[i] = 0
        
    print("Finished Initializing.")
    
    while finished_freq != len(time_set) :
        print(str(time) + "is processed at max " + str(song_length))
        for n in range(0, len(time_set)) :
            if time_setN[n] >= len(time_set[n]) :
                audio_list[n][time] = audio_list[n][time]
            elif time < time_set[n][time_setN[n]][0] :
                audio_list[n][time] = audio_list[n][time]
            elif time >= time_set[n][time_setN[n]][0] and time < time_set[n][time_setN[n]][1] :
                # playing
                audio_list[n][time] += 1
            elif time == time_set[n][time_setN[n]][1] :
                # playing
                audio_list[n][time] += 1
                time_setN[n] += 1
                if time_setN[n] == len(time_set[n]) :
                    finished_freq += 1
                    print(finished_freq)
            else :
                # playing
                time_setN[n] += 1
                if time_setN[n] == len(time_set[n]) :
                    finished_freq += 1
                    print(finished_freq)
        time += 1

    return audio_list

def make_empty_list(a = -1, b = -1, c = -1, d = -1) :
    result_list = []
    
    if a != -1 and b == -1:
        result_list = []
        
    elif b != -1 and c == -1 :
        for i1 in range(0, b) :
            result_list.append([])
            
    elif c != -1 and d == -1 :
        for i1 in range(0, b) :
            result_list.append([])
        for i1 in range(0, b) :
            for i2 in range(0, c) :
                result_list[i1].append([])
                
    else :
        for i1 in range(0, b) :
            result_list.append([])
        for i1 in range(0, b) :
            for i2 in range(0, c) :
                result_list[i1].append([])
        for i1 in range(0, b) :
            for i2 in range(0, c) :
                for i3 in range(0, d) :
                    result_list[i1][i2].append([])
    return result_list
        

    
file_names = "WAV_CUT/AMPM_song2.wav"
print("Loading file.\t: " + file_names)

y, sr = librosa.load(file_names, offset=0.0, duration = 10.0)

print("Loading finished.\t: " + file_names)

print("Get harmonics.\t: " + file_names)

y_h, y_p = librosa.effects.hpss(y)

print("Finished get harmonics.\t: " + file_names)

print("Get Frequencies.\t: " + file_names)

music = librosa.cqt(y, sr=sr, fmin=librosa.note_to_hz('C1'),
                    n_bins= 240, bins_per_octave= 12*4)

print("Dividing Instrument.\t: " + file_names)

print("Get little noise.\t: " + file_names)

small_th, large_th = get_threshold(music)

CQT_noise, CQT_harmonic = parse_noise(music, small_th)

print("Get little noise finish.\t: " + file_names)

print("Getting scale.\t: " + file_names)

scale_set, time_set = get_scale(CQT_harmonic)

print("Getting scale finish.\t: " + file_names)
'''
DTW_value = get_scale_simmilarity(scale_set)
'''
audio_list = converge_audio(scale_set, time_set, len(music))

print("Finish divide Instrument.\t: " + file_names)
plt.figure()
plt.plot(audio_list)
plt.show()
