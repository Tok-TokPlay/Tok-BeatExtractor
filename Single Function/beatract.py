import numpy as np
import librosa as lb

def MCC_with_DTW(sample, dest) :
    '''
    This function check simillarity of sound between sample and dest.
    Ignoring magnitude between sample and dest.
    Args : sample, dest
        sample - sound to compare.
        dest - sound to compare.
    Returns :
        simillarity of sample and dest.
    Raises : 
        nothing.
    '''
    # MCC : Magnitude Control Compare.
    largest_sample = 0.000000001
    for i in range(0, len(sample)) :
        if largest_sample < sample[i] :
            largest_sample = sample[i]
	
    largest_dest = 0.000000001
    for i in range(0, len(dest)) :
        if largest_dest < dest[i] :
            largest_dest = dest[i]
	
    # Comapre largest value and multiply to one.
    temp = []
    for i in range(0, len(dest)) :
        temp.append(dest[i] * largest_sample / largest_dest)
        D, wp = lb.dtw(sample, temp, subseq = True)
	
    # D[-1, -1] is simillarity of sounds.
    return abs(D[-1, -1])
		
def take_local_maximum(CQT_result, threshold) :
	'''
    Take local Maximum value range bigger then threshold.
    Args : CQT_result, threshold
		CQT_result : which picked up bigger then threshold.
		threshold : standard of picking value at CQT_result.
	Returhns : 
		list which value is 0 when smaller then threshold value or some value when bigger then threshold value.
    Raises : 
        nothing.
    '''
    high = []
    result = []
    for t in range(0, len(CQT_result[0])) :
        for i in range(0, len(CQT_result)) :
            if CQT_result[i][t] > threshold :
                # i th scale at time t is larger then threshold...
                high.append(i)
				# pick up.
        result.append(high)
        high = []
		# Add list to result and initialize high to empty list.
    return result


def get_threshold(CQT_result, seed = 0.75) :
    '''
    Return the threshold number for CQT_result with differential value.
    Args : CQT_result, seed
   		CQT_result - the list of CQT's output.
        seed - the seed of how far from standard value to mim / max values.
    Returns : 
		min / max value of threshold. threshold value.
    Raises : 
        nothing.
    '''
    result_list = []
    for f in range(0, len(CQT_result)) :
        for t in range(0, len(CQT_result[0])) :
            result_list.append(abs(CQT_result[f][t]))
	
    result_list.sort()
    # Copy List to sort result.
    sorted_tangent = []
    # Using Differential
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
