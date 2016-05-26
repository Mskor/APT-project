from os import listdir
import os
from os.path import isfile, join
import transform as trans

__author__ = 'oyakov'


RAW_DATA_FOLDER = 'E:\wave pack\\bearing_IMS\\4th_test'
S_AND_N_DATA_FOLDER = 'E:\wave pack\\bearing_IMS\\4th_test_split_and_normalized'


# write to filesystem
def dump(data, folder, filename, delim):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(join(folder, filename), 'a', encoding='utf-8') as f:
        for piece in data:
            f.write(str(piece) + delim)


def dump_bin(data, filename='E:\wave pack\\dump.txt', delim="\n"):
    with open(filename, 'wb') as f:
        for piece in data:
            f.write(bytearray(str(piece) + delim, encoding='utf-8'))


def rotate(data):
    line = []
    res = []
    for i in range(len(data[0])):
        for piece in data:
            line += [piece[i]]
        res.append(line)
        line = []
    return res


# extract channels from sound data text file
def read_file(filename, delim='\t'):
    with open(filename, encoding='utf-8') as file:
        lines = [s.split(delim) for s in file.read().splitlines()]
        array = []
        channels = rotate(lines)
        for channel in channels:
            array.extend([[float(val) for val in channel if val != '']])
        return array


def read_file_2(filename, delim='\t'):
    with open(filename, encoding='utf-8') as file:
        lines = [s.split(delim) for s in file.read().splitlines()]
        array = []
        channels = rotate(lines)
        for channel in channels:
            array.extend([float(val) for val in channel if val != ''])
        return array


def read_channel(filename, delim=' '):
    with open(filename, encoding='utf-8') as file:
        lines = [s.split(delim) for s in file.read().splitlines()]
        array = []
        for line in lines:
            array += [float(val) for val in line if val != '']
        return array


# read all data from raw_data_dir split into channels & normalize
def read_and_provide_channels():
    print('Reading folder: ' + RAW_DATA_FOLDER + '...')
    files = [f for f in listdir(RAW_DATA_FOLDER) if isfile(join(RAW_DATA_FOLDER, f))]
    for p_idx, piece in enumerate(files):
        print('{0} part of {1} parts is processed \r'.format(p_idx, len(files)))
        # split signal into the channels
        channels = read_file(join(RAW_DATA_FOLDER, piece), delim='\t')
        for ch_idx, channel in enumerate(channels):
            # normalize
            channel = trans.norm_1_0(channel)
            # write to output directory
            dump(channel,
                 'E:\wave pack\\bearing_IMS\\4th_test_split_and_normalized\\channel_{0}\\'.format(ch_idx),
                 str(piece),
                 delim=' ')
