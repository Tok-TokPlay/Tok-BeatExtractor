import matplotlib.pyplot as plt

def get_threshold(CQT_result, seed = 0.75) :
    '''
    This method or function return the threshold number for CQT_result.
    '''
    result_list = []
    for f in range(0, len(CQT_result)) :
        for t in range(0, len(CQT_result[0])) :
            result_list.append(abs(CQT_result[f][t]))
    result_list.sort()
    sorted_tangent = []
    for i in range(0, len(result_list) - 10) :
        sorted_tangent.append((result_list[i + 10] - result_list[i]) / 10)
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
            if sorted_tangent[i] > (1 - seed) * maximum_tangent :
                small_tangent_index = i
        if large_tangent_index == -1 :
            if sorted_tangent[i] > (seed) * maximum_tangent :
                large_tangent_index = i
    return result_list[small_tangent_index], result_list[large_tangent_index]

CQT_result = []
for i in range(0, 200) :
    CQT_result.append([])

for i in range(0, 200) :
    for j in range(0, 200) :
        CQT_result[i].append(i + j * j + 2 * j)
print("Calculating threshold...")
small, large = get_threshold(CQT_result)
result_list = []
for f in range(0, len(CQT_result)) :
    for t in range(0, len(CQT_result[0])) :
        result_list.append(abs(CQT_result[f][t]))
print("Sorting...")
result_list.sort()
print(small, large)
plt.figure()
plt.plot(result_list)
plt.show()
