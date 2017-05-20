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


def get_threshold(CQT_result, seed = 0.75, result_hop = 1000) :
    '''
    Return the threshold number for CQT_result with differential value.
    Args : CQT_result, seed, result_hop
   		CQT_result - the list of CQT's output.
        seed - the seed of how far from standard value to mim / max values. default is 0.75 and this value should be real value at 0.5 ~ 1.
		result_hop - ignore value to take tangent of values. default is 1000
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
    # to using Differential, get tangent values.
    for i in range(0, len(result_list) - result_hop) :
        sorted_tangent.append((result_list[i + result_hop] - result_list[i]) / result_hop)
        maximum_tangent = 0
        maximum_index = -1
        for i in range(0, len(sorted_tangent)) :
            if maximum_tangent < sorted_tangent[i] :
                maximum_tangent = sorted_tangent[i]
                maxumum_index = i
		
	small_tangent_index = -1
	large_tangent_index = -1
	# get result with calcuated tangent values.
	for i in range(0, len(sorted_tangent)) :
 		if small_tangent_index == -1 :
			if sorted_tangent[i] > (1 - seed) * maximum_tangent :
				small_tangent_index = i
		if large_tangent_index == -1 :
			if sorted_tangent[i] > (seed) * maximum_tangent :
				large_tangent_index = i

    return result_list[small_tangent_index], result_list[large_tangent_index]

def parse_noise(CQT_result, MAG_threshold) :
    '''
    parsing noise of CQT_result. result will be real harmonic sound which is bigger then threshold.
    Args : CQT_result, MAG_threshold
		CQT_result - Mixture of CQT_result that big sound and small sound.
		MAG_threshold - Standard for judge big and small.
    Returns : CQT_noise, CQT_harmonic
		CQT_noise - small sound which judged to noise sound.
		CQT_harmonic - big sound which judged to big sound.
    Raises : 
        nothing.
    '''
	# Make empty 2 by 2 list.
	# Dimension of output list is same as CQT_result (input list).
    CQT_noise = []
    CQT_harmonic = []
    for f in range(0, len(CQT_result)) :
        CQT_noise.append([])
        CQT_harmonic.append([])
	
    for f in range(0, len(CQT_result)) :
	# f is frequency ( Note, CQT values ).
        for t in range(0, len(CQT_result[0])) :
		# t is time.
            if abs(CQT_result[f][t]) > MAG_threshold :
			# if bigger then MAG_threshold...
                CQT_harmonic[f].append(CQT_result[f][t])
                CQT_noise[f].append(0)
            else :
			# if smaller then MAG_threshold
                CQT_harmonic[f].append(0)
                CQT_noise[f].append(CQT_result[f][t])
	
    return CQT_noise, CQT_harmonic



