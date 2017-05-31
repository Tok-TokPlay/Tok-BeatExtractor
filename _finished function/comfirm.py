'''
debugging console.
'''

import beatract as bt
import beatract_st_ver2 as bt2

'''
make_empty_list test code
'''

'''
test_list = bt.make_empty_list([3, 3, 3], [])
print (test_list)
'''

''' 
stage_note test code
'''

test_notes = \
[\
    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0],\
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],\
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],\
    [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1],\
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]]
note = bt.stage_note(test_notes)

print "============================note================================="
print("length of time : " + str(len(note)))
for i in range(0, len(note)):
    print(note[i])
print "============================note================================="

link_table, note_list, icoef_table, length_table = bt2.tie_note(note, 5)
print "============================link================================="
print("length of link_table : " + str(len(link_table)))
for i in range(0, len(link_table)):
    print(link_table[i])
print "============================link================================="
print(note_list)
print(icoef_table)
print(length_table)
print("Note Number = " + str(len(note_list)))