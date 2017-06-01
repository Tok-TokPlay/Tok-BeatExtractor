import numpy as np
import matplotlib.pyplot as plt


py = np.pi
t = np.arange(0, 256)
sig = np.sin(2 * py * ( 1250.0 / 10000.0 ) * t) + np.sin(2 * py * ( 625.0 / 10000.0 ) * t )
sp = np.fft.fft( sig )
plt.plot(t[0:256], 10 * np.log10(abs(np.fft.fft(sig))))
plt.show()





# 주파수를 보고 싶으면 sp 에는 np.fft.fft(실제 값들)
#freq = np.fft.fftfreq(t.shape[-1], 0.1)
# freq = np.fft.fftfreq(전체 frame 갯수, 초당 frame 입력 횟수의 역수)
#print(t.shape[-1])
#for i in freq2 :
#    print(i)

#plt.plot(freq, np.abs(sp) / t.shape[-1])
#크기는 샘플 수만큼 나눠줘야 합니다.
#plt.ylim([-0.1, 0.6])
#plt.grid()
#plt.xlabel("Frequency(Hz)")
#plt.ylabel("Magnitude")
#plt.show()
