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


data_from_files = []

for file_ in read_files("data","TDD"):
    data_from_single_file = []
    with open(file_ ,encoding='ISO-8859-1') as f:
        for line in f:
            data_from_single_file.append(line)
    data_from_files.extend(data_from_single_file[22:])

print(data_from_files[0])
print(data_from_files[1])



    