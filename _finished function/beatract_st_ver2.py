'''
This module act tie notes.
To use this module, just call tie note.
'''
def tie_note(note, threshold):
    '''
    tie notes which related to same instrument.
    Args: r_harmonic, note, far_th
        r_harmonic - harmonic magnitude list.
        note - note_set of harmonics.
        far_th - farnote's threshold.
    Return: link_table, note_list, icoef_table, length_table
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time0-1 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...],
              at time1-2 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...],
              at time2-3 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...],
              ...
              at time fin-1 - fin [...][...]...								   ...]
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
    Raise:
        nothing.
    '''
    #Initialize 4 table.
    link_table = []
    note_list = []
    icoef_table = []
    length_table = []
    #add first note to note_list
    for notes in range(0, len(note[0])):
        note_list.append([])
        note_list[notes].append(notes)

    # link note[0] and note[1] with stable_marriagement
    append_list(note, link_table, note_list, icoef_table, length_table, 0)
    for time in range(1, len(note)-1):
		# Stable marriagement -> link notes 1 : 1
        stable_marriagement(note[time], note[time+1], link_table, length_table, time, threshold)
		# Converge -> link notes n : 1
        coverage(note[time], note[time+1], link_table, note_list, icoef_table,\
		length_table, time, threshold)
		# Seperate -> link notes 1 : n
        seperate(note[time], note[time+1], link_table, note_list, icoef_table,\
		length_table, time, threshold)
		# renew 4 tables
        append_list(note, link_table, note_list, icoef_table, length_table, time)
    return link_table, note_list, icoef_table, length_table

def stable_marriagement(note_t1, note_t2, link_table, length_table, time, threshold):
    '''
	link note1 and note2 with smallest value and length_table with threshold.
	Args: note, link_table, note_list, icoef_table, length_table, time, threshold
		note_t1 - time1`s note. [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]]
		note_t2 - time2`s note. [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]]
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        length_table - plused or minused length of note`s location.
            [ coef 0 [4, -2, -1, ... 1, 3, 3],
              coef 1 [-1, -2, -1, ... 2, 3, 1],
              coef 2 [4, 4, 3, ... 2, -3, 1],
              ...
              coef t [2, 1, 0, ... 1, -2, -1] ]
		time - now processing time.
		threshold - threshold to acceptance of distance.
	Return:
	    Add to link_table
	Raise:
	    nothing
	'''
    print("A")

def coverage(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th): 
    print("A")

def seperate(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th):
    print("A")

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
def mid(note):
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

def distance(time1, time2):
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
    for i in range(0, len(time1)):
        difference.append([])
        # add empty list to difference to show i`th time1 notes and all time2 notes.
        for j in range(0, len(time2)):
            # add difference of time1[i] and time2[j]
            # just uclidean distance of two note`s average.
            difference[i].append(abs(mid(time1[i]) - mid(time2[j])))
    return difference
