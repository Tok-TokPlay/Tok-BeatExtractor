import struct
import os
import wave
import math
import numpy as np
import matplotlib.pyplot as plt


# Wave File = 0 ~ 20 Hz + 20 ~ 8000 Hz + 8000 ~ Hz Dat.
# So, 20 ~ 8000 Hz Data is remain, other Data is deleted.
# This will be utilzed with pre-processor.

#origin_file_name = "D:/Workspace/Python/GHeyKid_song.wav"
#changed_file_name = "D:/Workspace/Python/GHeyKid_song_pre_processored.wav"

origin_file_name = "WAV_ANALYS/GS_one_3579.wav"
changed_file_name = "WAV_ANALYS/Changed_GS_one_3579.wav"

origin_wav = wave.open(origin_file_name, "r")
changed_file_wav = wave.open(changed_file_name, "w")

song_framerate = float(origin_wav.getframerate())
song_nframes = origin_wav.getnframes()
song_nchannels = origin_wav.getnchannels()

comptype = "NONE"
compname = "not compressed"
sampwidth = 2

changed_file_wav.setparams((song_nchannels, sampwidth, song_framerate, song_nframes, comptype, compname))

local_maximum_check_value = 20
local_maximum_threshlod = 100

sampling_interval =  0.2
length = int(sampling_interval * song_framerate)
time_interval = sampling_interval / length

time_var = np.arange(0.0000, sampling_interval, time_interval)
freq = np.fft.fftfreq(len(time_var), time_interval)

#print(song_nchannels)
#print(str(freq[0]) + " " + str(freq[1]) + " " + str(freq[2]))

# I will use buffered_data to fft and calculating frequency.
# Then, i'll discard not in 20 ~ 8000 Hz
buffered_data = []
ch1_buffered_data = []
ch2_buffered_data = []
ch1_ffted_data = []
ch2_ffted_data = []
ch1_lo_max_data = []
ch2_lo_max_data = []
ch1_abs_data = []
ch2_abs_data = []
ch1_iffted_data = []
ch2_iffted_data = []

# Saving Data with wav format.
for i in range(0, song_nframes) :
    song_data = origin_wav.readframes(1)
    if(i % 500 == 0 and i != 0) :  
        # Print how many we came ( with % ).
        print("Task Processed : " + str(i / song_nframes * 100))
    if(i % length == 0 and i != 0) : 
        # if we gathered song_framerate * 0.0625 data, we fft this and saving.
        # fft moves time axis to frequency axis.
        buffered_data.append(song_data)
        ch1_buffered_data.append(struct.unpack("2h",buffered_data[len(buffered_data) - 1])[0])
        ch2_buffered_data.append(struct.unpack("2h",buffered_data[len(buffered_data) - 1])[1])

        ch1_ffted_data = np.fft.fft(ch1_buffered_data)
        ch2_ffted_data = np.fft.fft(ch2_buffered_data)
        for j in range(0, len(ch1_ffted_data)) :
            ch1_abs_data.append(abs(ch1_ffted_data[j]) / (len(ch1_ffted_data)))
            ch2_abs_data.append(abs(ch2_ffted_data[j]) / (len(ch2_ffted_data)))
        #Find Local Maximum.
        print("Start Finding Local Maximum in Task " + str(i / length))
        temp_ch1_dat = ch1_abs_data[0]
        temp_ch2_dat = ch2_abs_data[0]
        ch1_lo_max_data.append(0)
        ch2_lo_max_data.append(0)
        mode = True
        j = 0

        while j < (len(ch1_abs_data) - local_maximum_check_value) : # At all range of ffted data ( abs mean how large )
            if mode == True :
                if temp_ch1_dat < ch1_abs_data[j]  : # Discard not maximum
                    temp_ch1_dat = ch1_abs_data[j]
                    ch1_lo_max_data.append(0)
                    #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch1_abs_data[j - 1]) + "\t dB.")
                else :                               # Gathering If it is maximum
                    flag = True
                    for k in range(j, j + local_maximum_check_value - 1) :
                        if temp_ch1_dat < ch1_abs_data[k] and flag == True :
                            flag = False
                    if flag == True :
                        if ch1_abs_data[j] > local_maximum_threshlod :
                            temp_ch1_dat = ch1_abs_data[j]
                            ch1_lo_max_data.append(ch1_ffted_data[j - 1])
                            mode = False
                            #print("Colected frequency " + str(freq[j]) + "\twith " + str(ch1_abs_data[j - 1]) + "\t dB.")
                        else :
                            temp_ch1_dat = ch1_abs_data[j]
                            #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch1_abs_data[j - 1]) + "\t dB.")
                            ch1_lo_max_data.append(0)
                    else :                          # Discard if it is not maximum
                        temp_ch1_dat = ch1_abs_data[j]
                        #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch1_abs_data[j - 1]) + "\t dB.")
                        ch1_lo_max_data.append(0)
                        

            else :
                if temp_ch1_dat > ch1_abs_data[j]  : # Discard not maximum
                    temp_ch1_dat = ch1_abs_data[j]
                    ch1_lo_max_data.append(0)
                    #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch1_abs_data[j - 1]) + "\t dB.")
                else :                               # Gathering If it is maximum
                    temp_ch1_dat = ch1_abs_data[j]
                    flag = True
                    iflag = 0
                    for k in range(j, j + local_maximum_check_value - 1) :
                        if temp_ch1_dat > ch1_abs_data[k] and flag == True :
                            flag = False
                            iflag = k - j
                    if flag == False :
                        if iflag >= 2 :
                            for k in range(0, iflag-2) :
                                 ch1_lo_max_data.append(0)
                        elif iflag == 1 :
                            ch1_lo_max_data.append(0)
                        j = iflag + j - 1
                        mode = True
                        ch1_lo_max_data.append(0)
                    else :                          # Discard if it is not maximum
                        temp_ch1_dat = ch1_abs_data[j]
                        ch1_lo_max_data.append(0)
                        #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch1_abs_data[j - 1]) + "\t dB.")
            j = j + 1
        mode = True
        j = 0
        while j < (len(ch2_abs_data) - local_maximum_check_value) : # At all range of ffted data ( abs mean how large )
            if mode == True :
                if temp_ch2_dat < ch2_abs_data[j]  : # Discard not maximum
                    temp_ch2_dat = ch2_abs_data[j]
                    ch2_lo_max_data.append(0)
                    #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch2_abs_data[j - 1]) + "\t dB.")
                else :                               # Gathering If it is maximum
                    flag = True
                    for k in range(j, j + local_maximum_check_value - 1) :
                        if temp_ch2_dat < ch2_abs_data[k] :
                            flag = False
                    if flag == True :
                        if ch2_abs_data[j] > local_maximum_threshlod :
                            temp_ch2_dat = ch2_abs_data[j]
                            ch2_lo_max_data.append(ch2_ffted_data[j - 1])
                            mode = False
                            #print("Colected frequency " + str(freq[j]) + "\twith " + str(ch2_abs_data[j - 1]) + "\t dB.")
                        else :
                            temp_ch2_dat = ch2_abs_data[j]
                            #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch2_abs_data[j - 1]) + "\t dB.")
                            ch2_lo_max_data.append(0)
                    else :                          # Discard if it is not maximum
                        temp_ch2_dat = ch1_abs_data[j]
                        ch2_lo_max_data.append(0)
                        #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch2_abs_data[j - 1]) + "\t dB.")

            else :
                if temp_ch2_dat > ch2_abs_data[j]  : # Discard not maximum
                    temp_ch2_dat = ch2_abs_data[j]
                    ch2_lo_max_data.append(0)
                    #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch2_abs_data[j - 1]) + "\t dB.")
                else :                               # Gathering If it is maximum
                    temp_ch2_dat = ch2_abs_data[j]
                    flag = True
                    iflag = 0
                    for k in range(j, j + local_maximum_check_value - 1) :
                        if temp_ch2_dat > ch2_abs_data[k] and flag == True :
                            flag = False
                            iflag = k - j
                    if flag == False :
                        if iflag >= 2 :
                            for k in range(0, iflag-2) :
                                 ch2_lo_max_data.append(0)
                        elif iflag == 1 :
                            ch2_lo_max_data.append(0)
                        j = iflag + j - 1
                        mode = True
                    else :                          # Discard if it is not maximum
                        temp_ch2_dat = ch2_abs_data[j]
                        ch2_lo_max_data.append(0)
                        #print("Didn't Colected frequency " + str(freq[j]) + "\twith " + str(ch2_abs_data[j - 1]) + "\t dB."
            j = j + 1
                    
        #for j in range(0, len(ch1_ffted_data)) :
        #    ch1_abs_data.append(abs(ch1_ffted_data[j]) / (len(ch1_ffted_data) * 50))
        #    ch2_abs_data.append(abs(ch2_ffted_data[j]) / (len(ch2_ffted_data) * 50))
            # Normalizing the big number to small number.
        #    print(str(freq[j]) + "\tHz Ch1 : " + str(abs(ch1_ffted_data[j])) + "\tCh2 : " + str(abs(ch2_ffted_data[j])))
        #ffreq = freq[0:int(len(freq)/2)]
        #cc1 = ch1_abs_data[0:int(len(ch1_abs_data)/2)]
        #plt.plot(ffreq, cc1[0:len(ffreq)])
        #plt.grid(True)
        #print(str(freq[0]) + str(freq[1]) + str(freq[2]))
        #plt.show()
        #This is code for watching frequency with how wave length is big.
        #deleted = 0
        #for j in range(0, len(freq)) :
            #ch1_ffted_data[j] = ch1_ffted_data[j] * 0.6
            #ch2_ffted_data[j] = ch1_ffted_data[j] * 0.6
            #if freq[j] < 2000 or freq[j] > 8000 :
            #    ch1_ffted_data[j] = ch1_ffted_data[j] * 0.0001
            #    ch2_ffted_data[j] = ch2_ffted_data[j] * 0.0001
            #    deleted = deleted + 1
            #else :
            #    ch1_ffted_data[j] = ch1_ffted_data[j] * 2
            #    ch2_ffted_data[j] = ch1_ffted_data[j] * 2
        #print(str(deleted / length * 100) + "% was deleted")
            
        print("End Finding Local Maximum in Task " + str(i / length))
        ch1_iffted_data = np.fft.ifft(ch1_lo_max_data)
        ch2_iffted_data = np.fft.ifft(ch2_lo_max_data)
        print("Start Saving Local Maximum in Task " + str(i / length))
        print("Ch1 length " + str(len(ch1_iffted_data)) + " Ch2 length " + str(len(ch2_iffted_data)))
        print("Ch1 length " + str(len(ch1_lo_max_data)) + " Ch2 length " + str(len(ch2_lo_max_data)))
        for j in range(0, len(ch1_iffted_data)) :
            if ch1_iffted_data[j] > -32769 and ch1_iffted_data[j] < 32768 :
                if ch2_iffted_data[j] > -32769 and ch2_iffted_data[j] < 32768 :
                    changed_file_wav.writeframes(struct.pack('h', int(ch1_iffted_data[j])))
                    changed_file_wav.writeframes(struct.pack('h', int(ch2_iffted_data[j])))
        print("End Saving Local Maximum in Task " + str(i / length))
        print("=======================================================================")
        for j in range(0, len(ch1_lo_max_data) - 1)    :
            if ch1_lo_max_data[j] != 0 :
                print("Ch1 Data\t" + str(freq[j]) + "\t" + str(abs(ch1_lo_max_data[j])))
                
        for j in range(0, len(ch1_lo_max_data) - 1)    :
            if ch2_lo_max_data[j] != 0 :
                print("Ch2 Data\t"  + str(freq[j]) + "\t" + str(abs(ch2_lo_max_data[j])))
        print("=======================================================================")
            
        # Initializing Lists...
        ch1_buffered_data = []
        ch2_buffered_data = []
        ch1_ffted_data = []
        ch2_ffted_data = [] 
        ch1_abs_data = []
        ch2_abs_data = []
        ch1_lo_max_data = []
        ch2_lo_max_data = []
        ch1_iffted_data = []
        ch2_iffted_data = []
    else :
        buffered_data.append(song_data)
        ch1_buffered_data.append(struct.unpack("2h",buffered_data[len(buffered_data) - 1])[0])
        ch2_buffered_data.append(struct.unpack("2h",buffered_data[len(buffered_data) - 1])[1])
        #Take 1 data from original wav file.
changed_file_wav.close()
