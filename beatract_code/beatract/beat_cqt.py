'''
This Module using by beat extract.
And related to check some musical analysis.
'''

import os
import librosa as lb
import beat_tie as bt2
import numpy as np
import matplotlib.pyplot as plt
import sys
import wave
import struct

reload(sys)
sys.setdefaultencoding('utf-8')

def vocalization(mp3_file, mr_file, save_dir=-1, mp3_dir=-1, mr_dir=-1, ar_name=-1):
	######################### Control part ###########################################
    mp3_dir_flag = False
    mr_dir_flag = False
    save_dir_flag = False
    ar_flag = False

    if save_dir != -1:
        # Save to save_dir. if not, Save to mr directory.
        save_dir_flag = True

    if mp3_dir != -1:
        # find at mp3_dir. if not, find to same python folder.
        mp3_dir_flag = True

    if mr_dir != -1:
        # find at mp3_dir. if not, find to same python folder.
        mr_dir_flag = True

    if save_dir != -1:
        # Save file dir is not defined, save to mr folder file.
        save_dir_flag = True

    if ar_name != -1:
        # saving file name. if not, save with mp3_file(AR).mp3 or wav.
        ar_flag = True
    ######################### Control part ###########################################
    ######################### Naming part ############################################

    # mp3 file to wav files.
    if mp3_dir_flag:
        mp3_file_name = to_wav(mp3_dir, mp3_dir, mp3_file)
    else:
        mp3_file_name = to_wav("", "", mp3_file)
    # mr file to wav files.
    if mr_dir_flag:
        mr_file_name = to_wav(mr_dir, mr_dir, mr_file)
    else:
        mr_file_name = to_wav("", "", mr_file)
    # save file name to f_song and f_inst.
    f_song = mp3_file_name
    f_inst = mr_file_name

    if ar_flag:
        if save_dir_flag:
            ar_file = save_dir + "/" + ar_name
        else:
            ar_file = ar_name
    else:
        # Initialize ar_file name with "".
        ar_file = ""

        # For all split name with "." in file name...
        for string_number in range(0, len(mp3_file_name.split("."))-1):
            # Get all except like ".mp3".
            ar_file += mp3_file_name.split(".")[string_number]

        ar_file += "(AR).wav"
    f_vocal = ar_file
    ######################### Naming part ############################################

    print("Openning...")
    f_song_audio, f_song_sampling_rate = lb.load(f_song)
    f_inst_audio, _ = lb.load(f_inst)

    # Trim small size song.
    print("Trimming...")
    f_song_audio, _ = lb.effects.trim(f_song_audio)
    f_inst_audio, _ = lb.effects.trim(f_inst_audio)

    f_vocal_audio = []
    if len(f_song_audio) < len(f_inst_audio):
        length = len(f_song_audio)
    else:
        length = len(f_inst_audio)
    # Save with distance.
    for process in range(0, length):
        if process % 1000 == 0:
            print(str(process) + " / " + str(length))
        f_vocal_audio.append(f_song_audio[process] - f_inst_audio[process])
    '''
    plt.figure()
    plt.plot(f_song_audio[0:2000])
    plt.plot(f_inst_audio[0:2000])
    plt.plot(f_vocal_audio[0:2000])
    plt.show()
    '''
    lb.output.write_wav(f_vocal, np.asarray(f_vocal_audio), f_song_sampling_rate)

'''
    w_song = wave.open(f_song, "r") 
    w_inst = wave.open(f_inst, "r") 
    w_vocal = wave.open(f_vocal, "w") 
 
    song_framerate = float(w_song.getframerate()) 
    song_nframes = w_song.getnframes() 
 
    vocal_framerate = song_framerate 
    vocal_nframes = song_nframes 
    vocal_nchannels = w_song.getnchannels() 
    comptype = "NONE" 
    compname = "not compressed" 
    sampwidth = 2 
 
    # Set wav file parameter. 
    w_vocal.setparams((vocal_nchannels, sampwidth, vocal_framerate, vocal_nframes, comptype, \
    compname)) 
 
    if vocal_nchannels == 2: 
        # If channer is 2... 
        for processed in range(0, song_nframes): 
            # for all range of songs, add euclidean distance with 2 song. 
            if processed % 1000 == 0: 
                print str(processed) + " / " + str(song_nframes) 
            song_data = w_song.readframes(1) 
            inst_data = w_inst.readframes(1) 
            vocal_data = (struct.unpack("2h", song_data)[0] - struct.unpack("2h", inst_data)[0], \
            struct.unpack("2h", song_data)[1] - struct.unpack("2h", inst_data)[1]) 
            # if distance is in range of below... 
            if vocal_data[0] > -32769 and vocal_data[0] < 32768: 
                if vocal_data[1] > -32769 and vocal_data[1] < 32768: 
                    w_vocal.writeframes(struct.pack('h', int(vocal_data[0]))) 
                    w_vocal.writeframes(struct.pack('h', int(vocal_data[1]))) 
 
    # Close used files. 
    w_song.close() 
    w_inst.close() 
    w_vocal.close() 
'''
def to_wav(dir_name, save_dir, file_name, addable_option="-n"):
    '''
    Change any file to wav file to calculate well.
    if wav, doesn't process.
    Args : dir_name, save_dir, file_name
        dir_name - src directory name which file_name is in.
        save_dir - dest directory name which file_name.wav will be saved.
        file_name - to change file name. file name should not contaion "." more then 1.
        addable_option - "-y" or "-n" to yes / No.
    Returns:
        dest_file - destination file name.
    Raises:
        file does not exist.
        directory does not exist.
        But keep going process.
    '''
    # src name : dir_name + file_name + .mp3, .wmv etc...
    # dest name : save_dir + file_name + .wav

    if file_name.split(".")[-1] != "wav":
        src_file = dir_name + "/"  + file_name

        # if in case of file name has "."...
        dest_file = ""
        for string_number in range(0, len(file_name.split("."))-1):
            # Get all except like ".mp3".
            dest_file += file_name.split(".")[string_number]

        dest_file = save_dir + "/" + dest_file + ".wav"

        #ffmpeg starting with full_name and wav_name
        # do system call " ffmpeg -i 'src_file' 'dest_file' "
        os.system('ffmpeg ' + addable_option + ' -i ' +\
        '\'' + src_file + '\' ' + '\'' + dest_file + '\'')
        return dest_file

    else:
        src_file = save_dir + "/"  + file_name
        return src_file


def take_local_maximum(two_dimension_list, threshold):
    '''
    Take local Maximum value range bigger then threshold.
    Just cut values threshold * 100 with increase order.
    Args : CQT_result, threshold
        CQT_result : which picked up bigger then threshold.
        threshold : standard of picking value at CQT_result.
	Return :
		list which value is 0 when smaller then threshold value
			or some value when bigger then threshold value.
    Raises :
        nothing.
    '''
    high = []
    result = []
    for times in range(0, len(two_dimension_list[0])):
        for indexes in range(0, len(two_dimension_list)):
            if two_dimension_list[indexes][times] > threshold:
                # i th scale at time t is larger then threshold...
                high.append(indexes)
                # pick up.
        result.append(high)
        high = []
        # Add list to result and initialize high to empty list.
    return result

def get_threshold(CQT_result, seed=0.75):
    '''
    Return the threshold number for CQT_result with differential value.
    Args : CQT_result, seed, result_hop
        CQT_result - the list of CQT's output.
        seed - the seed of how far from standard value to mim / max values.
            default is 0.75 and this value should be real value at 0.5 ~ 1.
        result_hop - ignore value to take tangent of values. default is 1000
    Returns :
        threshold value.
	Raises :
        nothing.
    '''
    result_list = []
    for frequency in range(0, len(CQT_result)):
        for time in range(0, len(CQT_result[0])):
            result_list.append(abs(CQT_result[frequency][time]))

    result_list.sort()
    length = len(result_list)

    return result_list[int(length*seed)]

def parse_noise(CQT_result, MAG_threshold):
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
    for f in range(0, len(CQT_result)):
        CQT_noise.append([])
        CQT_harmonic.append([])

    for f in range(0, len(CQT_result)):
    # f is frequency ( Note, CQT values ).
        for t in range(0, len(CQT_result[0])):
        # t is time.
            if abs(CQT_result[f][t]) > MAG_threshold:
            # if bigger then MAG_threshold...
                CQT_harmonic[f].append(CQT_result[f][t])
                CQT_noise[f].append(0)
            else:
            # if smaller then MAG_threshold
                CQT_harmonic[f].append(0)
                CQT_noise[f].append(CQT_result[f][t])
    return CQT_noise, CQT_harmonic

def get_scale(CQT_harmonic):
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

    for f in range(0, len(CQT_harmonic)):
        scale_set.append([])
        time_set.append([])

    recording = False
    st = 0
    ft = 0
    temp = []
    for f in range(0, len(CQT_harmonic)):
        for t in range(0, len(CQT_harmonic[0])):
            if recording == True:
                if abs(CQT_harmonic[f][t]) == 0:
                    ft = t - 1
                    scale_set[f].append(temp)
                    time_set[f].append([st, ft])
                    recording = False
                    temp = []
                else:
                    temp.append(CQT_harmonic[f][t])
            else:
                if abs(CQT_harmonic[f][t]) != 0:
                    st = t
                    recording = True
                    temp.append(CQT_harmonic[f][t])
    return scale_set, time_set

def make_empty_list(dimension, to_make):
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
    if len(dimension) > 1:
        for dimension_number in range(0, dimension[-1]):
            to_make.append([])
            make_empty_list(dimension[0:(len(dimension)-1)], to_make[dimension_number])
            # Recursion part to 0 ~ len(dimension) - 2 with making empty list at to_make[i].
        return to_make
    elif len(dimension) == 1:
        for _ in range(0, dimension[0]):
            to_make.append([])
        return to_make
        # if len(dimension) is one, then stop recursion and return to_make list so
		# can process other part of functions.

def stage_note(r_harmonics):
    '''
    stage notes to make decision which notes are same instrumental.
    Args : r_harmonics
        r_harmonics - real harmonics value map with 0 which is smaller then threshold.
    Returns : note
        note - for all time sequence, clustering all notes to list.
    Raises :
        nothing
    '''
    note = []
    # Initialize note list.
    for times in range(0, len(r_harmonics[0])):
        note.append([])
        note_number = 0
        on_writing = False
        # Initialize note[] list and set on_writing to false, because start
		# must be start with not writing.
        for frequency in range(0, len(r_harmonics)):
            if r_harmonics[frequency][times] == 0:
                if on_writing:
                    on_writing = False
                    note_number += 1
                    # At writing some note to list, if meet 0 then stop writing and
					# get ready to input next note.
                    # if not writing, befores are
            else:
                if on_writing:
                    # Keep writing.
                    # writing which frequency is at "note_number"`s note.
                    note[times][note_number].append(frequency)
                else:
                    # if note doesn't write, then turn on write flag
					# ( on_writing ) and append list and "f".
                    on_writing = True
                    note[times].append([])
                    note[times][note_number].append(frequency)
    return note

def beatract(dir_name, file_name=-1, save_dir=-1, addable_option="-n", \
specific=4, threshold_length=8, show_graph=-1, save_graph=-1, debugmode=-1, \
time_variation=0.5, time_warping=60, inner_debug=-1):
    '''
    at given dir_name/file_name extract beat and save it to txt file at save to.
    Args:
    Return:
    Raise:
        nothing.
    '''
    # if file_name is default value, check all file in directory.
    if file_name == -1:
        file_names = os.listdir(dir_name)
    else:
        file_names = [file_name]

    # if save_dir is default value, save_dir is in source directory.
    if save_dir == -1:
        save_dir = dir_name

    # now is now beat extracting number.
    now = 0
    for file_name in file_names:
        now += 1
        if debugmode != -1:
            # if debugmode on, write debugging message to console.
            print("Strat extracting " + file_name + "... Now " + str(now) + " / "+  \
            str(len(file_names)))
        # y, sr for calculate seconds.
        y, sr = lb.load(dir_name + '/' + file_name)
        second = len(y) / sr

        time = 0
        real_output = []

        while second > 0:
            if second > time_warping:
                #Start from times * 60 and with 60 seconds.
                addable_option = addable_option + " -ss " + str(time_warping * time) \
                + " -t " + str(time_warping)

                #to Wav file with same name, so we can get just one file.
                dest_file = to_wav(dir_name, dir_name, file_name, addable_option)
                time += 1
                second -= time_warping
            else:
                #Start from times * 60 and with remain seconds.
                addable_option = addable_option + " -ss " + str(time_warping * time) \
                + " -t " + str(second)

                #to Wav file with same name, so we can get just one file.
                dest_file = to_wav(dir_name, dir_name, file_name, addable_option)
                second = 0
                time += 1

            # if want to extract some given length, give load to duration value.
            audio_list, sampling_rate = lb.load(dest_file, offset=0.0)
            if debugmode != -1:
                # if debugmode on, write debugging message to console.
                print("file opend..." + "... Now " + str(now) + " / " +  str(len(file_names))\
                + " " + file_name)

            music = lb.cqt(audio_list, sr=sampling_rate, fmin=lb.note_to_hz('C1'), \
            n_bins=60*specific, bins_per_octave=12*specific)

            if debugmode != -1:
                # if debugmode on, write debugging message to console.
                print("file CQT finished..." + "... Now " + str(now) + " / " + \
                str(len(file_names))\
                + " " + file_name)

            threshold = get_threshold(music)
            _, r_harmonic = parse_noise(music, threshold)

            if debugmode != -1:
                # if debugmode on, write debugging message to console.
                print("file CQT harmonics extracted..." + "... Now " + str(now) + " / " + \
                str(len(file_names))\
                + " " + file_name)

            note = stage_note(r_harmonic)


            if debugmode != -1:
                # if debugmode on, write debugging message to console.
                print("file tie_note..." + "... Now " + str(now) + " / " + \
                str(len(file_names))\
                + " " + file_name)

            _, note_list, icoef_table, _ = bt2.tie_note(note, threshold_length, \
            debug_mode=inner_debug)

            if debugmode != -1:
                # if debugmode on, write debugging message to console.
                print("file weightract..." + "... Now " + str(now) + " / " + \
                str(len(file_names))\
                + " " + file_name)

            weights = bt2.weightract(r_harmonic, note, note_list, icoef_table, \
            debug_mode=inner_debug)

            # Set Time variation for input values.
            real_weights = bt2.set_time_variation(weights, \
            get_music_time(sampling_rate, len(audio_list)), sampling_rate, \
            time_variation=time_variation)

            real_output += real_weights

        save_to(save_dir, file_name.split(".")[0] + ".txt", real_output)

        if debugmode != -1:
            print("finished extract file..." + "... Now " + str(now) + " / "+  str(len(file_names))\
            + " " + file_name)

        if show_graph != -1:
            # if show graph is on...
            plt.figure()
            plt.plot(real_output)
            plt.show()

        if save_graph != -1:
            # if save graph is on...
            plt.figure()
            plt.plot(real_output)
            plt.savefig(str(dir_name)+"/"+str(file_name.split(".")[0] + ".png"))

def get_music_time(sampling_rate, music_length):
    '''
    input music_length and sampling rate, and calculated music time.
    Args: sampling_rate, music_length
        sampling_rate - sampling rate of music. ( for example, 44100Hz / Minutes )
        music_length - audio list`s length for input music.
    Return: time
        time - music length with unit of second.
    Raise:
        nothing.
    '''
    # music length is total length of seconds * sampling_rate.
    # So just devide length with rate.
    return music_length / sampling_rate

def save_to(dir_name, file_name, weight_list, standard_output=50000):
    '''
    save file_name to dir_name txt file with given weights list.
    Args: dir_name, file_name, weight_list
    Return:
        nothing.
    Raise:
        nothing.
    '''
    # Check for files name.
    files = open(str(dir_name)+"/"+str(file_name), "w")
    # for all weigths, write in files.
    max_value = -1
    for weights in range(0, len(weight_list)):
        if weight_list[weights] > max_value:
            max_value = weight_list[weights]

    for weights in range(0, len(weight_list)):
        weight_list[weights] *= standard_output / max_value

    for weights in range(0, len(weight_list)):
        files.write(str(weight_list[weights] * standard_output / max_value)+ "\n")
    files.close()
