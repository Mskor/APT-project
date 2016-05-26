__author__ = 'oyakov'


def norm_1_0(data_channel):

    # shift data
    mn = min(data_channel)
    data = list(map(lambda x: x - mn, data_channel))

    # stretch data
    mx = max(data)
    data = list(map(lambda x: x * (1/mx), data))
    return data
