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
    if (x == 1) and (y == 1):
        return 0
    else:
        return x + y;

def sum3ops(i, j, k):
    a = F[i]
    b = F[j]
    c = F[k]
    d = []
    for l in range(0, 16):
        elem = sum2(a[l], b[l])
        elem = sum2(elem, c[l])
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
    for i in range(0, 16):
        for j in range(i+1, 16):
            for k in range(j+1, 16):
                opsum = sum3ops(i, j, k)
                if is_e(opsum):
                    fg.extend([[i,j,k]])
                    print("Full group: {0}, {1}, {2}".format(i, j, k))

    return fg

def analyze_groups(uform_dir):
    fg = find_full()
    filters = []
    for i in range (0, 16):
        filters.extend(dataprovider.read_file(uform_dir + "/filter{0}".format(i)))
    filters_t = feature_extractor.rotate(filters)
    for i in range (0, len(filters_t)):
        ptr = filters_t[i]

