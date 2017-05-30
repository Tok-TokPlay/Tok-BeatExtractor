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

def coverge(t0, t1, t2, th, t, link_table, converge_table)	:
	'''
	Converge link notes.
	Args : t0, t1, t2, th, t, link_table, converge_table
		t0, t1, t2 - note set which time is n-1, n, n+1.
		th - threshold which length acceptable.
		t - time n.
		link_table - linked information which is linked.
		converge_table - converge information which is linked.
	Return : link_table, converge_table
		link_table - appended linked information which is linekd.
		converge_table - appended converge information which is linked.
	'''	
	# Initialize difference and linked_length
	difference = distance(t1, t2)
	linked_length = link_length(t0, t1, linked_note)
	
	for i in range(0, len(t1)) : 
		# for all t1`s notes...
		if len(link_table[i]) != 0 :
			# if t1`s note is not null, add to converge table.
			converge_table[t+1][link_table[t][i][0]] += converge_table[t][i]
		else : 
			# if t1`s note is null, initialize it to 1.
			converge_table[t+1][j] = 1
			for j in range(0, len(t2)) : 
				# then, if i`th value is acceptable to all range of t2...
				if distance[i][j] < average(linked_length[i]) * th : 
					# link it and add to link table and converge table.
					link(i, j, link_table)
					converge_table[t+1][j] += converge_table[t][i]
	return link_table, converge_table

def sperate(t0, t1, t2, th, t, converge_table) :
	print("A")

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
	converge_table = []
	link_notes(note[0], note[1], link_table)
	# Below procedure will at 1 to note - 1, so need more job about 0 and note.
	for t in range(1, len(note) - 1) :
		# for all note in "note" list...
		link_table.append([])
		stable_marriagement(note[t-1], note[t], note[t+1], link_table[t-1], th)
		# link is uncompleted finished, so link which not linked.
				
		converge(note[t-1], note[t], note[t+1], th, t, link_table, converge_table)
		seperate(note[t-1], note[t], note[t+1], th, t, link_table, converge_table)

	return link_table

def all_linked(link_table, t) :
	'''
	Check link_table[t] is all linked.
	Args : link_table, t
		link_table - linked_information
		t - at time t
	Return : return_value
		return_value - if all note is linked, return True.
			else, return False.
	'''
	return_value = True
	for a in range(0, len(link_table[t])) :
		if len(link_table[t][a]) == 0 : 
			# If there exist some null linked value, return false.
			return_value = False
	return return_value

def link_notes(t0, t1, link_table) : 
	'''
	link t0, t1 with only distacne. At this moment, ignore far.
	Args : t0, t1, link_table
		t0, t1 - notes which will be linked.
		link_table - linked information which is linked.
	Return : link_table
		link_table - appended link_table`s link information.
	Raise : 
		nothing.
	'''
	# initialize linked length 
	linked_length = []

	# difference_i_j mean distance of t_i and t_j
	difference = distance(t0, t1)
	linked_length = []
	
	for a in range(0, len(t0)) :
		linked_length.append([])
		linked_length[a].append(100000)
		# 100000 is as big value which can cover all distance.
	
	# Initialize propse_queue, prefer_queue	
	difference = distance(t0, t1)
	
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
def append_list(note, link_table, note_list, icoef_table, length_table, time):
    '''
	append list from note and link_table, to note_list... etc.
	Args: note, link_table, note_list, icoef_table, length_table, time
	    note - note values of which frequency ( or real note ) are included.
			[ at time 0 [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]],
              at time 1 [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]],
              at time 2 [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]],
			  ...
              at time t [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]] ]
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        note_list - note list which represent instrumental.
            [ note_list 0 [0, 0, 0, ... 0, 1, 0],
              note_list 1 [1, 1, 1, ... 1, 1, 1],
              note_list 2 [2, 1, 2, ... 1, 1, 2],
              ...
              note_list t [t, t-1, t, ... t, t-1, t] ]
        icoef_table - inversed coefficient of notes. means, value`s number is sharing that
            harmonics magnitude value.
            [ coef 0 [1, 1, 1, ... 1, 3, 1],
              coef 1 [1, 2, 1, ... 2, 3, 1],
              coef 2 [1, 2, 1, ... 2, 3, 1],
              ...
              coef t [1, 1, 1, ... 1, 2, 1] ]
        length_table - plused or minused length of note`s location.
            [ coef 0 [4, -2, -1, ... 1, 3, 3],
              coef 1 [-1, -2, -1, ... 2, 3, 1],
              coef 2 [4, 4, 3, ... 2, -3, 1],
              ...
              coef t [2, 1, 0, ... 1, -2, -1] ]
	Return:
	    nothing
	Raise:
	    nothing
	'''
	# note_list append part...
    for note_number in range(0, len(note_list)):
        if note_list[note_number][-1] == -1:
    		# if finished with -1, we need to append -1 to assure finished instruments.
            note_list[note_number].append(-1)

    for link_number in range(0, link_table[time]):
        if len(link_table[time][link_number]) == 0:
    		# Case of empty list.
            for note_number in range(0, len(note_list)):
                if note_list[note_number][-1] == link_number:
                    note_list[note_number].append(-1)
        elif len(link_table[time][link_number]) == 1:
    		# Case of normal size ( 1 ) list.
            for note_number in range(0, len(note_list)):
                if note_list[note_number][-1] == link_number:
                    note_list[note_number].append(link_table[time][link_number])
        else:
    		# Case of size is larger then 2.
			# Must append some instruments.to_insert = 0
            for insert_number in range(0, len(note_list)):
                if note_list[insert_number][-1] == link_number:
                    to_insert = insert_number
                    break
            for _ in range(0, len(link_table[time][link_number])):
    			# for all value 0 to SIZE(== link_table[time][link_number])...
                note_list.insert(to_insert, [])
				# copy note_list[to_insert+1] to note_list[to_insert]
                for notes in range(0, note_list[to_insert+1]):
                    note_list[to_insert].append(note_list[to_insert+1][notes])
            for note_number in range(0, len(note_list)):
                if note_list[note_number][-1] == link_number:
                    note_list[note_number].append(link_table[time][link_number])
		# Above can`t catch new instrument started.
		# So we need to catch new instrument start like below.
        if link_number > 0:
            _link_number = link_number
		    # For case of new instrument start.
            while link_number > 0:
                if link_table[time][_link_number] != []:
    	    		# Ignore empty list to find real ins_num.
                    break
            ins_num = link_table[time][link_number][0] - link_table[time][_link_number][-1]
	    	# ins_num is absent_instrumental`s number + 1.
            for absent_number in range(0, ins_num -1):
                note_list.insert(link_number, [])
                for _ in range(0, len(note_list[link_number+1])-1):
    		    	# Add prefix note to -1 cause new instrument is started.
                    note_list[link_number].append(-1)
                note_list[link_number].append(absent_number)
	# note_list append part...
	# icoef_table append part...

