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
            [ at time 0 [1, 2, 3, 4], [6, 7, 8, 9], ... [211, 212, 213, 214, 215],
              at time 1 [2, 3, 4, 5, 6 ,7, 8], [10, 11, 12] ... [212, 213, 214, 215],
              ...
              at time n [2, 3 , 4, 5], [8, 9, 10, 11], ... [211, 212, 213, 214] ]
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
    difference = distance(note_t1, note_t2)
    propose_queue = make_queue(note_t1, note_t2, length_table, difference, threshold)
    prefer_queue = make_queue(note_t1, note_t2, length_table, difference, threshold)

    # i is index and value as same time.
    # j is value related to i.
    free, i, j = is_free_note(propose_queue, link_table)

    while not free:
        linked, linked_i = is_linked(link_table, j = propose_queue[i][j])
        delete_relation(propose_queue, i, j)
        if linked:
            if priority(prefer_queue, j, i) > priority(prefer_queue, j, linked_i):
                delete_link(link_table, linked_i, j)
                make_link(link_table, i, j)
        else:
            make_link(link_table, i, j)
        free, i, j = is_free_note(propose_queue, link_table)
def make_queue(note_t1, note_t2, length_table, difference, threshold):
    '''
    make propose queue ( prefer list ) for note_t1 to note_t2.
    Args:
    Return: prefer_list
        prefer_list -
    Raise:
        nothing
    '''
    prefer_list = []
    return prefer_list

def is_free_note(propose_queue, link_table):
    '''

    Args:
    Return:
    Raise:
    '''
    return False, -1, -1

def is_linked(link_table, i=-1, j=-1):
    '''

    Args: i, j, link_table
    Return: linked, linked_i
        linked - if given i or j are linked with some notes, return True, else return False.
        linked_i - if linked == True, return linked note`s list "note"`s index.( value )
            else, return -1
    Raise:
    '''

    return False, -1

def delete_relation(propose_queue, i, j):
    '''

    Args:
    Return:
    Raise:
    '''

def priority(prefer_queue, i, j):
    '''

    Args:
    Return:
    Raise:
    '''

def delete_link(link_table, i, j):
    '''

    Args:
    Return:
    Raise:
    '''

def make_link(link_table, i, j):
    '''

    Args:
    Return:
    Raise:
    '''

def coverage(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold):
    '''
    '''
    difference = distance(note_t1, note_t2)
    for note_number1 in range(0, len(note_t1)):
        linked, _ = is_linked(link_table, i=note_number1)
        if not linked:
            for note_number2 in range(0, len(note_t2)):
                acceptable = acceptable_note(difference, note_number1,\
                note_number2, time, threshold)
                if acceptable:
                    make_link(link_table, note_number1, note_number2)
                    break

def acceptable_note(difference, i, j, time, threshold):
    '''
    '''
    return False

def seperate(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold):
    '''
    '''
    difference = distance(note_t1, note_t2)
    for n1 in range(0, len(note_t1)):
        icoef = calc_icoef(icoef_table, note_list, n1)
        for n2 in range(0, len(note_t2)):
            if icoef > 1:
                if acceptable_note(difference, n1, n2, time, threshold):
                    make_link(link_table, n1, n2)
            else :
                break

def calc_icoef(icoef_table, note_list, n1):
    '''
    calculate icoef with time0 to time1`s note_list`s value is n1.
    stage location of note_list`s value, then return that location`s icoef_table
    '''
    return 0

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

def beatract(r_harmonics, note, link_table, note_list, icoef_table):
    '''
    Extract beat with some weights.
    Periodic instrument( note link ) will have low weights.
    Large sound will have high weights.
    Args: r_harmonics, note, link_table, note_list, icoef_table
    Return: beat_weights
    Raise:
         nothing
    '''
    periodic = []
    for note_number in range(0, len(note_list)):
        periodic.append(get_periodic(note_list[note_number]))

    weights = []
    for note_number in range(0, len(note_list)):
        weights.append([])
        for sequence in range(0, len(note_list[note_number])):
            weights[note_number].append([get_weights(note, note_list[note_number][sequence], \
            icoef_table[note_number][sequence])])
    real_beat = []
    for note_number2 in range(0, len(weights[0])):
        _sum = 0
        for note_number1 in range(0, len(weights)):
            _sum += weights[note_number1][note_number2]
        real_beat.append(_sum)
    return real_beat

def get_periodic(note_t1):
    '''

    Args:
    Return:
    Raise:
        nothing.
    '''

def get_weights(note, note_value, icoef_value):
   '''

    Args:
    Return:
    Raise:
        nothing.
   '''
