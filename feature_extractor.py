import uform as uf
from scipy.io.wavfile import read
import matplotlib.pyplot as plt


def dump(data, filename='E:\wave pack\\dump.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for piece in data:
            f.write(str(piece) + "\n")


filename = 'E:\wave pack\\about_time.wav'

fq, signal = read(filename)

signal = uf.shift8b(signal, -128)

u1 = uf.uform_dec(signal)
u2 = uf.uform_dec(signal, 2)
u3 = uf.uform_dec(signal, 3)
u10 = uf.uform_dec(signal, 10)
u100 = uf.uform_dec(signal, 100)
u1000 = uf.uform_dec(signal, 1000)
T, C = uf.roughen(u1000, 3)
dump(u1000)
dump(C, filename='E:\wave pack\\dump2.txt')
print(signal)

plt.plot(signal)
plt.show()


