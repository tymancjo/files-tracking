# following
# http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/

import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import time, sys, os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

matplotlib.use("TkAgg")

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
    # plt.ion()
    # plt.show()
    plt.draw()
    plt.pause(0.01)
    


def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    filename, ext = os.path.splitext(event.src_path)
    print(f"Its the {filename} with the extension {ext}")
    

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    plot_data(data_process(read_files("data","TDD")))

    # print(f"hey buddy, {event.src_path} has been modified")

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    # path = "."

    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    # kicking it off
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
        print("Folder watchdog ended!")