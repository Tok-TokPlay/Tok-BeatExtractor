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
        stable_marriagement(note[time], note[time+1], link_table, note_list, \
		icoef_table, length_table, time, threshold)

def stable_marriagement(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th):
    print("A")

def append_list(note, link_table, note_list, icoef_table, length_table, t ):
    print("A")

def coverage(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th): 
    print("A")

def seperate(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th):
    print("A")

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
