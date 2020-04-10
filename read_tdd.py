# this is a script to read a ttd files from given directory
# and process them. The TDD files comes from Yokogawa data recorders

import glob
import numpy as np
import matplotlib.pyplot as plt

def read_files(directory, files_ext):
    
    files_path = str(directory)+'/*.'+str(files_ext)
    
    print(f"reading from: {files_path}")

    list_of_files = glob.glob(files_path)
    list_of_files.sort()
    
    return list_of_files

def data_process(list_of_files):
    data_from_files = []

    for file_ in list_of_files:
        data_from_single_file = []
        with open(file_ ,encoding='ISO-8859-1') as f:
            for line in f:
                data_from_single_file.append(line)
        data_from_files.extend(data_from_single_file[22:])

    final_data = []
    final_marks = []

    for ix,data_line in enumerate(data_from_files):
        the_line = data_line.split("\t")
        clean_line = []
        # lets clean data in this line
        # starting from 3th (1st is time, 2nd is min, 3th is first max) 
        # andstepping by 2 - taking themax only
        for element in the_line[2::2]:
            # skipping 2 first as those are date and time
            element_value = float(element)

            # zeroing the big values 
            if element_value > 500:
                element_value = "X"
            
            clean_line.append(element_value)

        time_stamp = the_line[0].split(" ")[1][:-4]
        max_position = clean_line.index("X")
        # collecting final data
        final_marks.append(time_stamp)
        final_data.append(clean_line[:max_position])

    final_data = np.array(final_data)
    return final_marks, final_data

def plot_data(input_data):
    final_marks,final_data = input_data
    plt.clf()
    plt.plot(final_marks,final_data)
    plt.xticks( final_marks[::20], rotation='vertical')
    plt.ion()
    plt.show()

    
plot_data(data_process(read_files("data","TDD")))