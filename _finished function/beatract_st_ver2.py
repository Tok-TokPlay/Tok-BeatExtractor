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
    propose_queue = make_queue(note_t1, note_t2, length_table, difference, threshold, time)
    prefer_queue = make_queue(note_t2, note_t1, length_table, difference, threshold, time)

    # i is index and value as same time.
    # j is value related to i.
    free, i, j = is_free_note(propose_queue, link_table)

    while not free:
        linked, linked_i = is_linked(link_table, j=propose_queue[i][j])
        delete_relation(propose_queue, i, j)
        if linked:
            if priority(prefer_queue, j, i) > priority(prefer_queue, j, linked_i):
                delete_link(link_table, time, linked_i, j)
                make_link(link_table, time, i, j)
        else:
            make_link(link_table, time, i, j)
        free, i, j = is_free_note(propose_queue, link_table)

def make_queue(note_t1, note_t2, length_table, difference, threshold, time):
    '''
    make propose queue ( prefer list ) for note_t1 to note_t2.
    if note_t1 and note_t2`s length is smaller then before_length + threshold, append it.
    Args: note_t1, note_t2, length_table, difference, threshold
        note_t1, note_t2 - note_t1 is standard note and note_t2 is compared note.
        length_table - length information is saved here.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        difference - length between note_t1 and note_t2.
        threshold - threshold value which calculated at make decision.
        time - t1`s time. t2 mean "time+1".
    Return: prefer_list
        prefer_list - propose queue of note_t1 to note_t2.
        [ 0 th value`s priority is [0, 1, 2],
          1 th value`s priority is [1, 2, 3],
          2 th value`s priority is [2, 3, 4, 5],
          ...
          n th value`s priority is [n-2, n-1, n] ]
    Raise:
        nothing.
    '''
    # Initialize prefer_list with empty list.
    prefer_list = []
    for t1_number in range(0, len(note_t1)):
        # Add empty list at index of t1_number.
        prefer_list.append([])
        for t2_number in range(0, len(note_t2)):
            if get_length(length_table, time, t1_number) + threshold > \
            difference[t1_number][t2_number]:
                # Add prefer_list to index "t2_number".
                prefer_list[t1_number].append(t2_number)
    return prefer_list

def get_length(length_table, time, i):
    '''
    get length from length table which is linked with i th note at time "time-1" to "time".
    Args: length_table, time, i
        length_table - length information is saved here.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        time - time which will be used in when`s length.
        i - note`s index which note want to calculate.
    Return: length
        length - length_table
    Raise:
        nothing.
    '''
    # take all value in length_table`s time-1`s i th note`s length.
    average = 0
    for length_num in range(0, len(length_table[time-1][i])):
        average += length_table[time-1][i][length_num]
    # ... and return average of length sum.
    return average / len(length_table[time-1][i])

def is_free_note(propose_queue, link_table):
    '''
    Calculate is ther free note in link_table which is at propose_queue.
    Args: propose_queue, link_table
        propose_queue - propose queue of note_t1 to note_t2.
        [ 0 th value`s priority is [0, 1, 2],
          1 th value`s priority is [1, 2, 3],
          2 th value`s priority is [2, 3, 4, 5],
          ...
          n th value`s priority is [n-2, n-1, n] ]
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
    Return: Bool, i, j
        Bool - does linkable notes are exist.
        i - if linkable, t1`s notes index.
        j - if linkable, t2`s notes index.
    Raise:
        nothing.
    '''
    return False, -1, -1

def is_linked(link_table, i=-1, j=-1):
    '''
    Check if given i or j is linked in link_table, and return which is linked.
    Args: i, j, link_table
    Return: linked, linked_i
        linked - if given i or j are linked with some notes, return True, else return False.
        linked_i - if linked == True, return linked note`s list "note"`s index.( value )
            else, return -1
    Raise:
        nothing.
    '''

    return False, -1

def delete_relation(propose_queue, i, j):
    '''
    delete relation at propose_queue[i] which is linked with value "j"
    Args: propose_queue, i, j
    Return:
        nothing.
    Raise:
        nothing.
    '''
    # For all range in propose_queue[i]...
    for delete_number in range(0, len(propose_queue[i])):
        if propose_queue[i][delete_number] == j:
            del propose_queue[i][delete_number]
            break

def priority(prefer_queue, i, j):
    '''
    return j th priority at prefer_queue[i].
    Args: prefer_queue, i, j
    Return: priority
        priority - value which is MAX - index.
            if prioirity is large, index is small.
    Raise:
        nothing.
    '''
    # For all range in prefer_queue[i]...
    for prior in range(0, len(prefer_queue[i])):
        if prefer_queue[i][prior] == j:
            # length - prior is priority.
            return len(prefer_queue[i]) - prior

def delete_link(link_table, time, i, j):
    '''
    delete link at link_table[i]`s linked value "j"
    Args: link_table, i, j
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        i - time "time"`s index.
        j - time "time+"`s note index value.
    Return:
        nothing.
    Raise:
        nothing.
    '''
    # for all value in link_table.
    for delete_number in range(0, len(link_table[time][i])):
        if link_table[time][i][delete_number] == j:
            # delete which value is j in i th note`s link.
            del link_table[time][i][delete_number]

def make_link(link_table, time, i, j):
    '''
    make link at link_table[i]`s link value "j"
    Args: link_table, i, j
    Return:
        nothing.
    Raise:
        nothing.
    '''
    # Make link with at time "time", i`th notes to j.
    link_table[time][i].append(j)
    
def coverage(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold):
    '''
    converge which is not linked and have acceptable link notes.
    Args: note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold
    Return:
        nothing.
    Raise:
        nothing.
    '''
    difference = distance(note_t1, note_t2)
    for note_number1 in range(0, len(note_t1)):
        linked, _ = is_linked(link_table, i=note_number1)
        if not linked:
            for note_number2 in range(0, len(note_t2)):
                acceptable = acceptable_note(difference, note_number1,\
                note_number2, time, threshold)
                if acceptable:
                    make_link(link_table, time, note_number1, note_number2)
                    break

def acceptable_note(difference, i, j, time, threshold):
    '''
    Check acceptablility with difference[i][j] + threshold is in length acceptable at time.
    Args: difference, i, j, time, threshold
    Return: bool
        bool - if acceptable, return True, else return False.
    Raise:
        nothing.
    '''
    return False

def seperate(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold):
    '''
    Seperate if coef is lareger then 2 and have acceptable_note in range of length.
    Args: note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold
    Return:
        nothing.
    Raise:
        nothing.
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
    Args: icoef_table, note_list, n1
    Return: int
        int - calculation note_list`s nl icoef value.
    Raise:
        nothing
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
    before_i = 0
    for i in range(0, len(link_table[time])):
        if link_table[time][i][0] - link_table[time][before_i][-1] < 2 or i == 0:
            if len(link_table[time][i]) == 0:
                for j in range(0, len(note_list)):
                    if note_list[j][time] == i:
                        note_list[j].append(-1)
            elif len(link_table[time][i]) == 1:
                before_i = i
                for j in range(0, len(note_list)):
                    if note_list[j][time] == i:
                        note_list[j].append(link_table[time][i][0])
            else:
                before_i = i
                j = 0
                while j < len(note_list):
                    if note_list[j][time] == i:
                        for l in range(0, len(link_table[time][i]-1)):
                            copy_to(note_list, j, copy(note_list[j], link_table[time][i][l]))
                            copy_to(icoef_table, j, icoef_table[j])
                            copy_to(length_table, j, length_table[j])
                            j += 1
                        j += 1
        else:
            for k in range(link_table[time][before_i][-1]+1, link_table[time][i][0]):
                #copy_to(note_list, k, [-1,-1,-1 ... -1,k] for range time+1)
                #copy_to(icoef_table, k, [0, 0, 0 ... 0] for range time -1)
                #copy_to(length_table, k, [0, 0, 0 ... 0] for range time - 1)
                print("a")
    append_icoef(link_table, note_list, icoef_table)
    append_length(link_table, note_list, length_table)

def copy_to(dest_list, dest, src_list):
    '''
    copy src_list to dest_list[dest] with insert method.
    Args: dest_list, dest, src_list
    Return:
        nothing.
    Raises:
        nothing.
    '''

def append_icoef(link_table, note_list, icoef_list):
    '''
    append icoef_list with note_list and link_table.
    Args: link_table, note_list, icoef_list
    Return:
        nothing.
    Raises:
        nothing.    
    '''

def append_length(link_table, note_list, length_table):
    '''
    append length_table with note_list and link_table.
    Args: link_table, note_list, length_table
    Return:
        nothing.
    Raises:
        nothing.
    '''

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
    for i in range(0, len(note)):
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
    get note_t1`s periodic score.
    if note_t1 have many notes, score up.
    if note_t1 have periodical wave, score down.
    Args: note_t1
    Return: periodic_score
        periodic_score - score if note_t1 have many periodical wave or decompose many.
    Raise:
        nothing.
    '''

def get_weights(note, note_value, icoef_value):
    '''
    get weights of note`s with note_value and icoef_value.
    if icoef_value is large, weights are small.
    if value`s magnitude is large, weights are bigger.
    Args: note, note_value, icoef_value
    Return: weights
        weights - value which magnitude is big and which is sharing magnitude.
    Raise:
        nothing.
   '''
