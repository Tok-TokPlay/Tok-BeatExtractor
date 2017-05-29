def tie_note(note, th) :
	'''
	ti
	'''

def stable_marriagement(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th) :
    print("A")

def append_list(note, link_table, note_list, icoef_table, length_table, t ) :
    print("A")

def coverage(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th) : 
    print("A")

def seperate(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time,th) :
    print("A")

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

def distance(time1, time2) :
