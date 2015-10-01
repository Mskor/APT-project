import uform as uf
from os import listdir
from os.path import isfile, join
from scipy.io.wavfile import read
import matplotlib.pyplot as plt


def dump(data, filename='E:\wave pack\\dump.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for piece in data:
            f.write(str(piece) + "\n")


def rotate(data):
    line = []
    res = []
    for i in range(len(data[0])):
        for piece in data:
            line += [piece[i]]
        res.append(line)
        line = []
    return res


def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        lines = [s.split('\t') for s in file.read().splitlines()]
        array = []
        for line in lines:
            array += [float(val) for val in line]
        return array


def read_folder(folder, filterfunc=lambda x: x):
    print('Reading folder: ' + folder + '...')
    result = []
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    print('{0} files found.'.format(len(onlyfiles)))
    filteredfiles = filterfunc(onlyfiles)
    print('Applied filter, {0} out of {1} files will be processed.'.format(len(filteredfiles), len(onlyfiles)))
    for fname in filteredfiles:
        print('Progress: %.3f%%       \r' % (100*(filteredfiles.index(fname) + 1)/len(filteredfiles)), end="")
        result += read_file(join(folder, fname))
    return result


b = read_folder('C:\\Users\\oyakov\Downloads\\bearing_IMS\\1st_test', lambda x: x)
b = uf.shift8b(b, 0.1)
# u = uf.uform_dec(b, 100)
# T, C = uf.roughen(u, 100)
# figs, axes = plt.subplots(nrows=4, ncols=4)
# i = 0
# D = rotate(C)
# for axis in axes:
#     for ax in axis:
#         ax.plot(D[i])
#         i += 1

plt.plot(b)
plt.show()
