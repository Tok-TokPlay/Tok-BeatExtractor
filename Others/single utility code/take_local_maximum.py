def take_local_maximum(CQT_result, threshold) :
    high = []
    result = []
    for t in range(0, len(CQT_result[0])) :
        for i in range(0, len(CQT_result)) :
            if CQT_result[i][t] > threshold :
                # i th scale at time t is larger then threshold...
                high.append(CQT_result[i][t])
        result.append(high)
        high = []
    return result


sample = []
sample_temp = []
for i in range(0, 500) :
    for t in range(i, i + 20) :
        sample_temp.append(t)
    sample.append(sample_temp)
    sample_temp = []
print(len(sample))
print(len(sample[i]))
print(sample[-1][-1])
result = take_local_maximum(sample, 500)
for i in range(0, len(result) - 1) :
    print(result[i])
