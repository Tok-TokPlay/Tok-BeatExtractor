import numpy as np
import matplotlib.pyplot as plt


Ts = 0.01	        				# sampling interval
Fs = 1/Ts					        # sampling rate 	

time = np.arange(0.0, 5.0, Ts)
# 마지막에 smapling Timing 을 넣으면 된다.

resultTest1 = 1 * np.sin(2 * np.pi * 1 * time)
resultTest2 = 2 * np.sin(2 * np.pi * 5 * time)
resultTest3 = 4 * np.sin(2 * np.pi * 10 * time)
resultTest4 = 2 * np.sin(2 * np.pi * 8 * time)
resultTest5 = 8 * np.sin(2 * np.pi * 7 * time)
resultTest6 = 1 * np.sin(2 * np.pi * 12 * time)

y = resultTest1 + resultTest2 + resultTest3 + resultTest4 + resultTest5 + resultTest6
# 합성 파형

n = len(y) 					# length of the signal
k = np.arange(n)
T = n/Fs
freq = k/T 					# two sides frequency range
freq = freq[range(int(n/2))] 			# one side frequency range

temp_db = []
temp_hz = []

Y = np.fft.fft(y)/n 				# fft computing and normalization
Y = Y[range(int(n/2))]
j = 0;

for i in range(0, int(n/2)) :                   # 
    if abs(Y)[i] > 0.1 :
        temp_db.append(abs(Y)[i])
        temp_hz.append(freq[i])
        j = j + 1

for i in range(0, j - 1) :
    print(temp_db[i])
    print(temp_hz[i])



fig, ax = plt.subplots(2, 1)
ax[0].plot(time, y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[0].grid(True)

ax[1].plot(freq, abs(Y), 'r', linestyle=' ', marker='^') 
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
ax[1].vlines(freq, [0], abs(Y))
ax[1].grid(True)
plt.show()
    
