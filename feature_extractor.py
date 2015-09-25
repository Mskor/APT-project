import scipy
from scipy.io.wavfile import read
from scipy.signal import hann
from scipy.fftpack import rfft


def extract(filename='F:\wave pack\Casio-CZ-5000-Synth-Bass-C1.wav'):

    fq, data = read(filename)
    data = [x for [x, _] in data]

    window = hann(10000)
    data = data[0:10000] * window

    mags = abs(rfft(data))

    mags = 20 * scipy.log10(mags)
    mags = mags[::100]
    return mags

def rms(data):
    return

def remove_noise(data, order):
    a = [data[i::i+len(data//order)] for i in range(order)]


