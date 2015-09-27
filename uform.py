"""
Module docstring here
"""

__author__ = 'oyakov'

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
    return list(map(lambda x: x + factor, data))

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

    # Calculate F * I an then reduce N rank matrix to N-dimensional vector with (+) operation
    return [sum(i) for i in [list(zipwith(fi, I, lambda x, y: y if x else -y)) for fi in F]]


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

    P = max([max(list(map(lambda x: abs(x), ui))) for ui in u])

    T = [i*P/k for i in range(k + 1)]

    return T, [list(map(lambda x: int(round(k * x / P)) if x != 0 else 0, ui)) for ui in u]
