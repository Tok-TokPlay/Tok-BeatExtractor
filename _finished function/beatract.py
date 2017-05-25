import numpy as np
import librosa as lb
import os

def to_wav(dir_name, save_dir, file_name) : 
	'''
	Change any file to wav file to calculate well.
	Args : dir_name, save_dir, file_name
		dir_name - src directory name which file_name is in.
		save_dir - dest directory name which file_name.wav will be saved.
		file_name - to change file name. file name should not contaion "." more then 1.
	Returns :
		nothing. save file?
	Raises : 
		file does not exist.
		directory does not exist.	
		But keep going process.
	'''
	# src name : dir_name + file_name + .mp3, .wmv etc...
	# dest name : save_dir + file_name + .wav
	src_file = dir_name + "/"  + file_name	
	dest_file = save_dir + "/" + file_name.split(".")[0] + ".wav"
	
	#ffmpeg starting with full_name and wav_name
	# do system call " ffmpeg -i 'src_file' 'dest_file' "
	os.system('ffmpeg -i ' + '\'' + src_file + '\' ' + '\'' + dest_file + '\'')

for filename in filenames :
	# add full_name dir_name.
	# actually full_name is full path of file name.

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

def get_scale(CQT_harmonic) :
	'''
	input CQT_harmonics and decompose it to scalse set and it's play tim.
	magnitude which smaller then threshold will be deleted to 0.
	Args : CQT_harmonics ( list )
		CQT_harmonics - noise removed harmonics which magnitude are over threshold.
	Returns : scale_set, time_set ( list )
		sacle_set - gathered multi-dimension list which magnitude are over threshold. ( 0 removed list )
		time_set - time sacle is start is time_set[i][0], time scale is finish is time_set[1]
	Raises : 
		Nothing
	'''
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

def get_scale_simmilarity(scale_set) :
	'''
	take scale and calculate simmilarity with DTW of each scale set.
	Args : scale_set ( list )
		scale_set - set of values which magnitude over threshold. ( Real Note of music. )
	Returns : DTW_value.
		DTW_value - 
	Raises :
		nothing
	'''
	scale_list = []
	DTW_value = []
	for f in range(0, len(scale_set)) :
		for t in range(0, len(scale_set[f])) :
			scale_list.append(scale_set[f][t])
			DTW_value.append([])
	for i in range(0, len(scale_list)) :
		for j in range(0, len(scale_list)) :
			if j < i :
				DTW_value[i].append(DTW_value[j][i])
			else : 
				DTW_value[i].append(MCC_with_DTW(scale_list[i], scale_list[j]))
	return DTW_value

def make_empty_list(a = -1, b = -1, c = -1, d = -1) :
	'''
	take empty list dimension. -1 is not using dimension.
	Args : 
		empty list dimension. -1 = not using ( default )
	Returns : 
		multi dimension empty list.
	Raises :
		nothing
	'''
	result_list = []
	# One Dimension list.
	if a != -1 and b == -1:
		result_list = []
	# Two Dimension list.
	elif b != -1 and c == -1 :
		for i1 in range(0, b) :
			result_list.append([])
	# Three Dimension list.
	elif c != -1 and d == -1 :
		for i1 in range(0, b) :
			result_list.append([])
		for i1 in range(0, b) :
			for i2 in range(0, c) :
				result_list[i1].append([])
	# Four Dimension list.
	else :
		for i1 in range(0, b) :
			result_list.append([])
		for i1 in range(0, b) :
			for i2 in range(0, c) :
				result_list[i1].append([])
		for i1 in range(0, b) :
			for i2 in range(0, c) :
				for i3 in range(0, d) :
					result_list[i1][i2].append([])
	# Can make it with recursive function with dimension list.
	return result_list

def make_empty_list_recursion(dimension, to_make)	:
	'''
	take empty list dimension with list of "dimension", make empty list, return it.
	Args : dimension[], to_make[][]...
		dimension - list of dimension to make empty list.
		to_make - list to make empty list in it.
	Returns : to_make
		to_make - input parameter to make empty list.
	Raises : 
		nothing.
	'''
	if len(dimension) > 1 :
		for i in range(0, dimension[-1]) : 
			to_make.append([])
			make_empty_list_recursion(dimension[0:(len(dimension)-2)], to_make[i])
			# Recursion part to 0 ~ len(dimension) - 2 with making empty list at to_make[i].
	elif len(dimension) == 1 : 
		for i in range(0, dimension[0]) :
			to_make.append([])
		return to_make	
		# if len(dimension) is one, then stop recursion and return to_make list so can process other part of functions.

def stage_note(r_harmonics) : 
	'''
	stage notes to make decision which notes are same instrumental.
	Args : r_harmonics
		r_harmonics - real harmonics value map with 0 which is smaller then threshold.
	Returns : note_map
		note_map - for all time sequence, clustering all notes to list.
	Raises : 
		nothing
	'''
	note = []
	# Initialize note list.
	for t in range(0, len(r_harmonics)) :
		note.append([])
		note_number = 0
		on_writng = False
		# Initialize note[] list and set on_writing to false, because start must be start with not writing.
		for f in range(0, len(r_harmonics[0])) :
			if harmonic[f][t] == 0 : 
				if on_writing :
					on_writing = False
					note_number += 1					
					# At writing some note to list, if meet 0 then stop writing and get ready to input next note.
					# if not writing, befores are 
			elif : 
				if on_writing : 
					# Keep writing.
					# writing which frequency is at "note_number"`s note.
					note[t][note_number].append(f)
				elif : 
					# if note doesn't write, then turn on write flag ( on_writing ) and append list and "f".
					on_writing = True
					note[t].append([])
					note[t][note_number].append(f)
	return note


