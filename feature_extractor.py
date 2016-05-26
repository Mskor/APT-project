import uform as uf
import math
from os import listdir
import os
from os.path import isfile, join, exists
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn import svm
import numpy as np
import dataprovider

MEAN = 0.0
RAW_DATA_FOLDER = 'D:\Research\\bearing_IMS\\2nd_test'
DATA_FOLDER = 'D:\Research\\bearing_IMS_split\\2nd_test_precise\\channel_0\\'


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


def read_file(filename, delim='\t'):
    with open(filename, encoding='utf-8') as file:
        lines = [s.split(delim) for s in file.read().splitlines()]
        array = []
        channels = rotate(lines)
        for channel in channels:
            array.extend([[float(val) for val in channel if val != '']])
        return array


def read_channel(filename, delim=' '):
    with open(filename, encoding='utf-8') as file:
        lines = [s.split(delim) for s in file.read().splitlines()]
        array = []
        for line in lines:
            array += [float(val) for val in line if val != '']
        return array


def seek_folder(folder):
    print('Reading folder: ' + folder + '...')
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    return onlyfiles


def mean(data):
    return sum(data) / len(data)


def calc():
    files = seek_folder(DATA_FOLDER)

    for f_idx, file in enumerate(files):
        print('{0} part of {1} parts is processed \r'.format(f_idx, len(files)))
        chunk = read_channel(join(DATA_FOLDER, str(file)))
        print('Calculating U-form...')
        u = uf.uform_dec(chunk, 16)
        print('Roughening...')
        #T, C = uf.roughen(u[0], 5)
        print('Rotate...')
        D = rotate(u)
        print('Dump...')
        for fil_idx, filtr in enumerate(D):
            dump(filtr,
                 'E:\wave pack\\bearing_IMS_split\\4th_test_precise\\channel_0_uform_1\\',
                 'filter{0}.txt'.format(fil_idx),
                 delim=' ')
        os.system('cls')


def prep():
    files = seek_folder(RAW_DATA_FOLDER)

    for p_idx, piece in enumerate(files):
        print('{0} part of {1} parts is processed \r'.format(p_idx, len(files)))
        channels = read_file(join(RAW_DATA_FOLDER, piece), delim='\t')
        global MEAN
        if p_idx == 0:
            MEAN = round(mean([mean(channel) for channel in channels]), 5)

        for ch_idx, channel in enumerate(channels):
            uf.shift8b(channel, 0.0-MEAN)
            dump(channel,
                 'E:\wave pack\\bearing_IMS_split\\2nd_test\\channel_{0}\\'.format(ch_idx),
                 str(piece),
                 delim=' ')


def precise_prep():
    files = seek_folder(RAW_DATA_FOLDER)

    s = []
    length = 20480 * len(files)
    for p_idx, piece in enumerate(files):
        print('{0} part of {1} parts is processed \r'.format(p_idx, len(files)))
        channels = read_file(join(RAW_DATA_FOLDER, piece), delim='\t')
        if p_idx == 0:
            s = [sum(channel) for channel in channels]
        else:
            s = list(uf.zipwith([sum(channel) for channel in channels], s, lambda x, y: sum([x, y])))

    _mean = ([si/length for si in s])

    for p_idx, piece in enumerate(files):
        print('{0} part of {1} parts is processed \r'.format(p_idx, len(files)))
        channels = read_file(join(RAW_DATA_FOLDER, piece), delim='\t')

        for ch_idx, channel in enumerate(channels):
            uf.shift8b(channel, 0.0 - _mean[ch_idx])
            dump(channel,
                 'E:\wave pack\\bearing_IMS_split\\2nd_test_precise\\channel_{0}\\'.format(ch_idx),
                 str(piece),
                 delim=' ')
    return s


def plot():
    gs = gridspec.GridSpec(4, 4)
    fig = plt.figure()
    for i in range(0, 16):
        filt = read_channel('E:\wave pack\\bearing_IMS\\2nd_test_extracted_features\channel_0_uform_4\\masses{0}.txt'.format(i), delim=' ')
        m = round(mean(filt), 3)
        filt = [round(fi, 3) for fi in filt]
        # sigma = []
        # for val_idx, val in enumerate(filt):
        #     o = 0.0
        #     for j in range(0, val_idx):
        #         o += (filt[j] - m) * (filt[j] - m)
        #     sigma.append((math.sqrt(o / (val_idx + 1))))
        # print(i)
        # # T, C = uf.roughen(filt, 10)
        ax = plt.subplot(gs[i//4, i%4])
        # ax.plot(filt)
        # smean = mean(sigma)
        # sko = [s - smean for s in sigma[200:]]
        ax.plot(filt)
        # clf = svm.SVR(kernel='rbf', C=100, gamma=0.0000001)
        # X = np.asarray([i for i in range(0, len(filt))]).reshape(len(filt), 1)
        # y = clf.fit(X, filt).predict(X)
        # ax.plot(y)
        #ax.plot(C)
        fig.add_subplot(ax)
    plt.show()


#              #
#              #
# CODE REFINERY#
#              #

def prepare_data():
    # raw data read, parsed into the channels
    # and is written into the filesystem
    dataprovider.read_and_provide_channels()


def extract_features():
    for i in range (0,4):
        files = seek_folder('D:\Research\\bearing_IMS\\2nd_test_split_and_normalized\\channel_{0}\\'.format(i))

        for f_idx, file in enumerate(files):
            print('{0} part of {1} parts is processed \r'.format(f_idx, len(files)))
            chunk = read_channel(join('D:\Research\\bearing_IMS\\2nd_test_split_and_normalized\\channel_{0}\\'.format(i), str(file)))
            print('Calculating U-form...')
            u = uf.uform_dec(chunk, 4)
            print('Rotate...')
            D = rotate(u)
            print('Dump...')
            for fil_idx, filtr in enumerate(D):
                dump(filtr,
                     'D:\Research\\bearing_IMS\\2nd_test_uform\\channel{0}_uform_16\\'.format(i),
                     'filter{0}.txt'.format(fil_idx),
                     delim=' ')
            os.system('cls')

#################################################################

"""
Module docstring here
"""

__author__ = 'oyakov'
import dataprovider, os
###############################################
#                Definitions                  #
###############################################

# Primary parameter of the extraction algorithm
# It will specify dimension of resulting U-spectre
N = 16

# Filter alphabet is a square matrix of rank N
F = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1],
    [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0],
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
]


###############################################
#            Auxiliary functions              #
###############################################

def invert(a):
    if a == 0:
        return 1
    else:
        return 0


def invert_op(oper):
    return [invert(i) for i in oper]


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def zipwith(x, y, f):
    """f: {xi}, {yi}, g -> {g xi yi}"""
    for i in range(0, len(x)):
        yield f(x[i], y[i])


def shift8b(data, factor):
    """
    Shift data array with the factor value
    :param data:
    :param factor:
    :return:
    """
    for idx, num in enumerate(data, start=0):
        data[idx] = round(num + factor, 5)

def sum2(x, y):
    if (x == 0) and (y == 0):
        return 0
    else:
        return 1;

def sum3ops(i, j, k):
    d = []
    for l in range(0, 16):
        elem = sum2(i[l], j[l])
        elem = sum2(elem, k[l])
        d.extend([elem])
    return d


def mul2(x, y):
    if (x == 1) and (y == 1):
        return 1
    else:
        return 0;


def mul3ops(i, j, k):
    d = []
    for l in range(0, 16):
        elem = mul2(i[l], j[l])
        elem = mul2(elem, k[l])
        d.extend([elem])
    return d

def is_e(oper):
    for i in range(0, 15):
        if oper[i] != 1:
            return False
    return True


###############################################
#              U-transformation               #
###############################################


def uform(data):
    """
    Computes an U-form of given data.
    :param data: a numerical sequence {xi} c f(t); f(t) - signal.
    :return: U-representation of numerical seqeunce denoted as data.
    """
    # Split into N pieces
    data = list(chunks(data, len(data) // N))

    # Integrate pieces get N-dimensional vector
    I = [sum(i) for i in data]

    # Calculate F * I and then reduce N rank matrix to N-dimensional vector with (+) operation

    u = []
    temp = []

    for fi in F:
        for idx, i in enumerate(I):
            if fi[idx]:
                temp.extend([i])
            else:
                temp.extend([-i])
        u.extend([temp])
        temp = []

    uf = []

    for ui in u:
        uf.extend([sum(ui)])

    return uf
    #return [round(sum(i), 3) for i in [list(zipwith(fi, I, lambda x, y: y if x else -y)) for fi in F]]


def uform_dec(data, K=1):
    """
    Computes an U-form of given signal decomposition. Decomposition is a signal fragmentation into K equal parts
    :param data:
    :return:
    """

    decomposition = list(chunks(data, len(data) // K))

    # TODO: need to implement concurrent calculation of the following
    # Wrapper executor objects? Any Python lib?
    return [uform(di) for di in decomposition]


###############################################
#                Roughening                   #
###############################################


def roughen(u, k):
    """

    :param u:
    :param k:
    :return:
    """

    # Find maximal absolute value in U-representation
    P = max([abs(uf) for uf in u])

    # Form a list of intervals with respect to roughening factor k
    T = [i * P / k for i in range(k + 1)]

    return T, list(map(lambda x: int(round(k * x / P)) if x != 0 else 0, u))

###############################################
#                Groups                       #
###############################################


def find_full():
    fg = []
    for i in range(1, 16):
        for j in range(i+1, 16):
            for k in range(j+1, 16):
                opsum = sum3ops(F[i], F[j], F[k])
                if is_e(opsum):
                    fg.extend([[i,j,k]])
                    print("Full group: {0}, {1}, {2}".format(i, j, k))

    return fg


def analyze_groups(uform_dir):
    full_groups = find_full()
    filters = []
    for i in range (0, 16):
        filters.extend([dataprovider.read_file_2(uform_dir + "/filter{0}.txt".format(i), ' ')])
    filters_t = rotate(filters)

    masses = []
    for i in range(0, len(filters_t)):
        mass = []
        ptr = filters_t[i]
        for cur_group in full_groups:
            fg_image = find_fg_image(ptr, cur_group)
            m = 0.0
            for idx in range(1, len(fg_image)):
                if fg_image[idx] != 0:
                    m += ptr[idx]
            mass.append(m)
        masses.append(mass)
    masses_t = rotate(masses)
    for idx, ms in enumerate(masses_t):
        dump(ms,
             'D:\Research\\bearing_IMS\\2nd_test_masses\\',
             "masses{0}.txt".format(idx),
             ' ')


def find_fg_image(data, full_group):
    d = data[full_group[0]] * data[full_group[1]] * data[full_group[2]]
    x = []
    y = []
    z = []
    if data[full_group[0]] > 0:
        x = F[full_group[0]]
    else:
        x = invert_op(F[full_group[0]])
    if data[full_group[1]] > 0:
        y = F[full_group[1]]
    else:
        y = invert_op(F[full_group[1]])
    if data[full_group[2]] > 0:
        z = F[full_group[2]]
    else:
        z = invert_op(F[full_group[2]])
    if d > 0:
        return mul3ops(x, y, z)
    elif d < 0:
        return sum3ops(x, y, z)
    else:
        return None


#
# ###########MAIN FLOW###############################

#prepare_data()
#extract_features()
#plot()

analyze_groups('D:\Research\\bearing_IMS\\2nd_test_uform\channel0_uform_16')
