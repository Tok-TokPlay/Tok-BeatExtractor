def parse_noise(CQT_result, MAG_threshold) :
    CQT_noise = []
    CQT_harmonic = []
    for f in range(0, len(CQT_result)) :
        CQT_noise.append([])
        CQT_harmonic.append([])

    for f in range(0, len(CQT_result)):
        for t in range(0, len(CQT_result[0])):
            if CQT_result[f][t] > MAG_threshold :
                CQT_harmonic[f].append(CQT_result[f][t])
                CQT_noise[f].append(0)
            else :
                CQT_harmonic[f].append(0)
                CQT_noise[f].append(CQT_result[f][t])

    return CQT_noise, CQT_harmonic


CQT_result = []
for i in range(0, 50) :
    CQT_result.append([])
    
for i in range(0, 50) :
    for j in range(0, 50) :
        CQT_result[i].append(abs(i-j))
print("Generating Sample Finish.")
CQT_noise, CQT_harmonic = parse_noise(CQT_result,20)

for f in range(0, 50) :
        print(str(CQT_noise[f]) + " is noise.")
        
for f in range(0, 50) :
        print(str(CQT_harmonic[f]) + " is harmonic.")
        
