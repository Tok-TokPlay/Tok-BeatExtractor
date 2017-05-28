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
			else : 
				if on_writing : 
					# Keep writing.
					# writing which frequency is at "note_number"`s note.
					note[t][note_number].append(f)
				else : 
					# if note doesn't write, then turn on write flag ( on_writing ) and append list and "f".
					on_writing = True
					note[t].append([])
					note[t][note_number].append(f)
	return note

def mid(note) :
	'''
	Input note set and return average of some vector or return a remarkable values.
	Args : note
		note - list of vector which represent some note.
	Returns : average
		average - average of vector or remarkable values.
	Raises : 
		nothing	
	'''
	average = 0
	for i in range(0, len(note)) :
		average += note[i]
	# just return average of note`s contents.
	return average / len(note)

def distance(time1, time2)	:
	'''
	compare note1 and note2 then return some distance of 2 notes.
	Args : time1, time2
		time1, time2 - notes list of at time1 and time2
	Return : difference
		difference - list of all distance of mid(time1[i]) and mid(time2[j])
	Raises :
		nothing
	'''
	difference = []
	# initialize return value "difference" with empty list
	for i in range(0, len(time1)) :
		difference.append([])
		# add empty list to difference to show i`th time1 notes and all time2 notes.
		for j in range(0, len(time2)) :
			# add difference of time1[i] and time2[j]
			# just uclidean distance of two note`s average.
			difference[i].append(abs(mid(time1[i]) - mid(time2[j])))
	return difference

def link_length(t0, t1, linked_note) : 
	'''
	linked_length information about t0 and t1 with link table "linked_note"
	Args : t0, t1, linked_note	
		t0, t1 - note set which want to know about linked length. 
			For specific, t1's order of length.
		linked_note - linke information table of t0 and t1.
	Return : linked_length
		linked_length - link information of t0 and t1.
			This list is sorted by t1, for example...
			linke_length = [ [10, 8], [4], [2, 3] ] means
				t1[0]'s linked_length is 10 and 8,
				t1[1]'s linked_length is 4 ... etc.
	Raises : 
		nothing.
	'''
	# initialize linked length 
	linked_length = []

	# difference_i_j mean distance of t_i and t_j
	difference = distance(t0, t1)
	
	for i in range(0, len(t1)) :
		linked_length.append([])
		# linked_length[i] mean link length which linked with t1[i].
		for a in range(0, len(linked_note)) :
			for b in range(0, len(linked_note[a])) :
				if linked_note[a][b][1] == i :
					# linked_note[a] mean link with t0[a]
					# linked_note[a][b] mean b`th link with t0[a], so linked_note[a][b][1] mean t1`s note.
					linked_length[i].append(difference[linked_note[a][b][0]][i])
					# append difference01[# of t0`s note][# of t1`s note]

	return linked_length
	
	
def farnote(t0, t1, t2, linked_note,th) :
	'''
	compare t1 and t2 list notes and return if t1 and t2 can be linkable all notes.
	this function is abstract check of far information.
	Args : t0, t1, t2, linked_note, th
		t0, t1, t2 - the note list which time is 0, 1, 2.
		linked_note - list of linked note`s pair list. 
			linked_note[i] = [i, j] mean i`th note is linked with j`th note.
		th - threshold. notes can be link with in range of this threshold.
	Return : 
		bool type. if linkalbe, return true, if not, return false.
	Raises : 
		nothing.
	'''
	# difference_i_j mean distance of t_i and t_j
	difference = distance(t1, t2)
		
	t1_before_length = link_length(t0, t1, linked_note)
	
	can_link = 0
	# can_link mean # of linkable note number
	# if all note are linkable, can_link == len(t1)
	for i in range(0, len(t1)) :
		for j in range(0, len(t2)) :
			if difference[i][j] < t1_before_length[i] + th :
				# if t1`s i th note is close to t2`s j th notes, then linkable.
				can_link += 1
				break

	if can_link == len(t1) :
		return True
	else :
		return False
def tie_note(r_harmonic, note, far_th) : 
	'''
	tie notes which related to same instrument.
	Args : r_harmonic, note, far_th
		r_harmonic - harmonic magnitude list.
		note - note_set of harmonics.
		far_th - farnote's threshold.
	Return : link_table
		link_table - tied notes which is related to some other note.
			bundle of notes are other represent of instrument.
			[ at time0-1 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...]
			  at time1-2 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...] 
			  at time2-3 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...]
			  ...
			  at timefin-1-fine[...][...]...								   ...]
	Raise : 
		nothing.
	'''
	link_table = []
	# Below procedure will at 1 to note - 1, so need more job about 0 and note.
	for t in range(1, len(note) - 1) :
		link_table.append([])
		if len(note[t]) == len(note[t+1]) :
			if farnote(note[t-1], note[t], note[t+1], link_table[t-1], far_th) : 
				# -1 +1 like as soon as overlaped then seperate, or finished then start.
				print("A")
			else :
				# standard state.
				# Do Stable Mariagement with t and t+1
				print("A")
		elif len(note[t]) > len(note[t+1]) : 
			if farnote(note[t-1], note[t], note[t+1], link_table[t-1], far_th) :
				# Overlapped.
				print("A")
			else : 
				# Instrument finished.
				print("A")
		else : 
			if farnote(note[t-1], note[t], note[t+1], link_table[t-1], far_th) : 
				# Seperated.
				print("A")
			else : 
				# Instrument start.
				print("A")

	return link_table

def average( _list ) : 
	'''
	calcuate list's average. list must be numerical.
	Args : _list
		_list - numeric value's list or one value.
	Return : mean
		mean - average of list.
	Raise :
		nothing.
	'''
	if(type(_list) == type([])) :
	# if input is list. 
		summed = 0
		# initialize summed.
		for i in range(0, len(_list)) : 
			summed += _list[i]
			# Calculated all sum of _list
		return summend/len(_list)	
	else : 
	# if input is not list
		return _list

def prefer_queue(t1, t2, linked_length, difference, th) : 
	'''
	make queue which will using at stable marriagement argorithms.
	Args : t1, t2, linked_length, difference
		t1, t2 - note list. t1 is standard note, so t1's prefer list about t2.
		linked_length - t0 and t1's linekd length. will be using calculate acceptance.
		difference - t1 and t2's length table. will be using calculate acceptance.
		th - acceptance of value of length.
	Return : propse_queue
		propose_queue - ordered queue having priority from t1 to t2.
	Raise : 
		nothing.
	'''
	# initialize queue and info list.
	propose_queue = []
	length_info = []
	for a in range(0, len(t1)) :
		propose_queue.append([])
		length_info.append([])
		# add [] size of t1's length.
		# ordered by t1.
		for b in range(0, len(t2)) : 
			if average(linked_length[a]) * th > difference[a][b] : 
				# if a and b's length is acceptable, append to queue.
				propose_queue[a].append(b)
				length_info[a].append(difference[a][b])
	# sorting propse_queue with length_info.
	for i in range(0, len(propose_queue)) :
		for a in range(0, len(propose_queue[i]) - 1) :
			for b in range(a+1, len(propose_queue[i])) :
				# At propose_queue[i], sort list propose_queue[i] with order of length_info, increase. 
				if length_info[i][a] > length_info[i][b] :
					# Swap length_info 
					temp = length_info[i][a]
					length_info[i][a] = lenth_info[i][b]
					length_info[i][b] = temp
						
					# Swap propose_queue
					temp = propose_queue[i][a]
					propose_queue[i][a] = propose_queue[i][b]
					propose_queue[i][b] = temp
	
	return propose_queue
	
def is_free_note(a, link_table, propose_queue) : 
	'''
	find which doesn't link note and that note is accpetable.
	make decision with ...
		1. if a have doesn't link note
		2.if that note`s propose_queue is empty
		3. if any other linkable notes...
	Args : a, link_table, propose_queue
		a - note list which will be linked.
		link_table - which is linked or not information.
		propse_queue - a's propse_queue. ordered by small distance.
	Return : can_link, i, j
		can_link - bool type return value which exiest linkable note.
		i - t1's index of note which doesn`t have link with t2.
		j - t2's index of note which i`s highest priority.
	Raise : 
		nothing.
	'''
	for i in range(0, len(a)) :
		# for all note in a...
		if len(link_table[i]) == 0 :
			# if a[i]`s link is null...
			if len(propoese_queue[i]) != 0 : 
				# if a[i]`s propese_queue[i] is not null...
				# return from small index.
				return True, i, propose_queue[i][0]
	# if all index is linked or have no more propse queue, can't link.
	return false, -1, -1

def is_linked(linked_table, i = -1, j = -1) : 
	'''
	check if i or j is not -1, not -1 value`s link information return.
	linked mean does i or j is linked, and if linked, return _i which is linked index.
	Args : i, j, linked_table
		i - if not -1, check linked_table[i] have link.
		j - if not -1, check linked_table[_i][j] have link.
		linked_table - 
	Return : linked, _i
		linked - 
		_i - 
	Raise : 
		nothing.
	'''
	if i != -1 : 
		# if input is i...
		if len(linked_table[i]) == 0 :
			# if i`th table is null, then doesn`t link.
			return False, -1
		else :
			# if i`th table is not null, return 1`st j value.
			return True, linked_table[i][0]
	elif j != -1 : 
		for a in range(0, len(linked_table)) :
			for b in range(0, len(linked_table[a])) :
				# at a`th linked_table, if a`th linked_table has value...
				if j == linked_table[a][b] : 
					# and that value is j, return
					return True, a
		return False, -1

def delete_queue(i, j, propose_queue) :
	'''
	delete propose_queue[i]`s j value.
	Args : i, j, propose_queue
		i - which will deleted number of index in queue.
		j - which will deleted number of notes in queue[i].
		propose_queue - deleted_queue
	Return : propse_queue
		propse_queue - deleted queue
	Raise : 
		nothing.
	'''
	for a in range(0, len(propose_queue[i])) : 
		if propose_queue[i][a] == j : 
			del(propose_queue[i][a])
			# if propose_queue[i][a] is same as j, then delete j.
	return propose_queue
	
def link(i, j, link_table) :
	'''
	link i`th note of t1 and j`th note of t2 at link_table.
	Args : i, j, link_table
		i - i`th note of t1
		j - j`th note of t2
		link_table - link information of notes.
	Return : link_table
		link_table - append link notes list information.
	Raise : 
		nothing.
	'''
	link_table[i].append(j)
	# link at link_table
	return link_table
	
def delete_link_table(i, j, link_table) : 
	'''
	delete i`th notes j value in link_table.
	Args : i, j, link_table
		i - i`th note of t1
		j - j value in t2
		link_table - link information of notes.
	Return : 
		link_table - appended link notes list information.
	Raise : 
		nothing.
	'''
	for b in range(0, len(link_table[i])) : 
		if link_table[i][b] == j : 
			del(link_table[i][b])
			# if link_table[i] have j, then delete.
	return link_table
	
def queue_index(queue, i, j) : 
	'''
	find j value in queue[i]
	Args : queue, i, j
		queue - priority queue of notes length.
		i - index of queue.
		j - value of queue[i] have.
	Return : index_of_j
		index_of_j - j in queue[i]`s index. if doesn't exist, return -1
	Raise : 
		nothing.
	'''
	for a in range(0, len(queue[i])) : 
		if queue[i][a] == j : 
			# if queue[i] has j, then return "index of j"
			return a
	# if note exist, return -1
	return -1

def stable_marriagement(t0, t1, t2, linked_note,th) : 
	'''
	link note1 and note2 with smallest value.
	Args : t0, t1, t2, linked_note, th
		t0, t1, t2 - before, now, after note list.
		linked_note - linked lnformation which note is linked and which note is not linked.
		th - adaptable value of linkinf distance.
	Return : link_table
		link_table - tied notes which is related to some other note.
			bundle of notes are other represent of instrument.
			[ at time0-1 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...]
			  at time1-2 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...] 
			  at time2-3 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...]
			  ...
			  at timefin-1-fine[...][...]...								   ...]
			Same as tie_note's returns.
	Raise : 
		nothing.	
	'''
	# Initialize link_table	
	link_table = []
	for a in range(0, len(t1)) : 
		link_table.append([])
	
	# Initialize propse_queue, prefer_queue	
	linked_length = link_length(t0, t1, linked_note)
	difference = distance(time1, time2)
	
	propose_queue = prefer_queue(t1, t2, linked_length, difference, th)
	prefer_queue = prefer_queue(t2, t1, linked_length, difference, th)
	
	free, i, j = is_free_note(t1, link_table, propose_queue)
	# free - does t1 can link to t2.
	# In word, t1 has free note and that note have not null propose_queue, return free note index i and 
	# i`th first value j.
	while not free :
		# if linkable...
		linked, _i = is_linked(j = proposed_queue[i][j], linked_table = link_table)
		propose_queue = delete_queue(i, j, propose_queue)
		# check if linkable j is free and delete i, j pair in propose queue.
		if linked : 
			if queue_index(prefer_queue, j, i) < queue_index(prefer_queue, j, _i) :
				# if linkable and j`th i  prefer index is smaller then j`th _i prefer index, delete _i and link i.
				# _i is linked value with j.
				delete_link_table(_i, j, link_table)
				link(i, j, link_table)
		else : 
			# if linkable j is free, link it.
			link(i, j, link_table)
		# initialize free and i, j.
		free, i, j = is_free_note(t1, link_table, propose_queue)
	return link_table
