import struct
import os
import math
import numpy
import matplotlib.pyplot as plt

def cosine_similarity(v1,v2):
    sumxx = 0
    sumxy = 0
    sumyy = 0
    for i in range(0, len(v1) - 1) :
        x = v1[i]
        y = v2[i]
        sumxx = sumxx + x * x
        sumyy = sumyy + y * y
        sumxy = sumxy + x * y
    return sumxy / math.sqrt(sumxx * sumyy)

full_filename = []
filenames = os.listdir("D:/Workspace/Python/TXT_OUT/All Files")
for filename in filenames:
    full_filename.append(os.path.join("D:/Workspace/Python/TXT_OUT/All Files", filename))

fileNumber = 0
i = 1
largest_length_file = 0
largest_length = 0
a = []

for j in range(0, len(full_filename) - 1 ) :
    f = open(full_filename[j],"r")
    str = f.read()
    if largest_length < len(str) :
        largest_length = len(str)
        largest_length_file = j
    f.close()

f = open(full_filename[largest_length_file],"r")
str = f.read()
for c in str :
    a.append(int(c))
f.close()

for filename in full_filename :
    f = open(filename,"r")
    str = f.read()
    i = 0
    for c in str :
        a[i] = a[i] + int(c)
        i = i + 1
    f.close()
b = []

for j in range(0, len(a)-1) :
    b.append(a[j] / (len(full_filename) - 1))

thresholds = 0.0
base_thresholds = 0.00
largest_result_result = 0
largest_thresholds = 0

for k in range(0, 100) :
    d = []
    print(k)
    thresholds = base_thresholds + ( k * 1 / 100 )
    for j in range(0, len(b)-1) :
        if b[j] > thresholds :
            d.append(1)
        elif b[j] > thresholds * 19 / 20 :
            d.append(19 / 20)
        elif b[j] > thresholds * 18 / 20 :
            d.append(18 / 20)
        elif b[j] > thresholds * 17 / 20 :
            d.append(17 / 20)
        elif b[j] > thresholds * 16 / 20 :
            d.append(16 / 20)
        elif b[j] > thresholds * 15 / 20 :
            d.append(15 / 20)
        elif b[j] > thresholds * 14 / 20 :
            d.append(14 / 20)
        elif b[j] > thresholds * 13 / 20 :
            d.append(13 / 20)
        elif b[j] > thresholds * 12 / 20 :
            d.append(12 / 20)
        elif b[j] > thresholds * 11 / 20 :
            d.append(11 / 20)
        elif b[j] > thresholds * 10 / 20 :
            d.append(10 / 20)
        elif b[j] > thresholds * 9 / 20 :
            d.append(9 / 20)
        elif b[j] > thresholds * 8 / 20 :
            d.append(8 / 20)
        elif b[j] > thresholds * 7 / 20 :
            d.append(7 / 20)
        elif b[j] > thresholds * 6 / 20 :
            d.append(6 / 20)
        elif b[j] > thresholds * 5 / 20 :
            d.append(5 / 20)
        elif b[j] > thresholds * 4 / 20 :
            d.append(4 / 20)
        elif b[j] > thresholds * 3 / 20 :
            d.append(3 / 20)
        elif b[j] > thresholds * 2 / 20 :
            d.append(2 / 20)
        elif b[j] > thresholds * 1 / 20 :
            d.append(1 / 20)
        else :
            d.append(0.00000001)
    result = []
    for j in range(0, len(full_filename) - 1 ) :
        e = []
        f = open(full_filename[j],"r")
        str = f.read()
        for c in str :
            e.append(int(c))
        f.close()
        result.append(cosine_similarity(d[0 :len(e) - 1], e))
    result_result = 0
    for j in range(0, len(result)-1)    :
        result_result = result_result + result[j]
    if largest_result_result < result_result :
        largest_thresholds = thresholds
        largest_result_result = result_result
    print(largest_thresholds)
    print(largest_result_result / (len(result)-1))
    
    
    
'''
for j in range(0,len(result) - 1) :
    print(result[j])
'''
thresholds = largest_thresholds
for j in range(0, len(b)-1) :
    if b[j] > thresholds :
        d.append(1)
    elif b[j] > thresholds * 19 / 20 :
        d.append(19 / 20)
    elif b[j] > thresholds * 18 / 20 :
        d.append(18 / 20)
    elif b[j] > thresholds * 17 / 20 :
        d.append(17 / 20)
    elif b[j] > thresholds * 16 / 20 :
        d.append(16 / 20)
    elif b[j] > thresholds * 15 / 20 :
        d.append(15 / 20)
    elif b[j] > thresholds * 14 / 20 :
        d.append(14 / 20)
    elif b[j] > thresholds * 13 / 20 :
        d.append(13 / 20)
    elif b[j] > thresholds * 12 / 20 :
        d.append(12 / 20)
    elif b[j] > thresholds * 11 / 20 :
        d.append(11 / 20)
    elif b[j] > thresholds * 10 / 20 :
        d.append(10 / 20)
    elif b[j] > thresholds * 9 / 20 :
        d.append(9 / 20)
    elif b[j] > thresholds * 8 / 20 :
        d.append(8 / 20)
    elif b[j] > thresholds * 7 / 20 :
        d.append(7 / 20)
    elif b[j] > thresholds * 6 / 20 :
         d.append(6 / 20)
    elif b[j] > thresholds * 5 / 20 :
        d.append(5 / 20)
    elif b[j] > thresholds * 4 / 20 :
        d.append(4 / 20)
    elif b[j] > thresholds * 3 / 20 :
        d.append(3 / 20)
    elif b[j] > thresholds * 2 / 20 :
        d.append(2 / 20)
    elif b[j] > thresholds * 1 / 20 :
        d.append(1 / 20)
    else :
        d.append(0.00000001)

e = []
f = open("D:/Workspace/Python/TXT_OUT/AMPM_song3_0.txt","r")
str = f.read()
for c in str :
    e.append(int(c))
f.close()

print(cosine_similarity(d[0 :len(e) - 1], e))

time = numpy.arange(0.0, 30.0, 0.02)

plt.plot(time,d[0:1500])
plt.show()
