import matplotlib.pyplot as plt

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


sample = []
for i in range(0, 200) :
    sample.append([])

for i in range(0, 200) :
    for j in range(0, 200) :
        if (j > 75 and j < 100) or j < 25 or ( j > 125 and j < 175)  :
            sample[i].append(j)
        else :
            sample[i].append(0)


scale_set, time_set = get_scale(sample)

for i in range(0, len(scale_set)) :
    for j in range(0, len(scale_set[i])) :
        print(str(i) + "\tth frequency, " + str(j) + "\tth scale : "+ str(scale_set[i][j]))
        print(str(i) + "\tth frequency, " + str(j) + "\tth scale is at "+ str(time_set[i][j]))
