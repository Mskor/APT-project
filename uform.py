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


###############################################
#              U-transformation               #
###############################################


def uform(data, L, K):
    """

    :param data: a numerical sequence {xi} c f(t)
    :param L: number of resulting spectral coefficients for each (D o I) {xi}; {xi} c f(t) application
    :param K: number of levels of decomposition
    :return:
    """
    # Split into N pieces
    data = list(chunks(data, len(data) // L))

    # Integrate pieces get N-dimensional vector
    I = [sum(i) for i in data]

    # Calculate F x I =
    d = [list(zipwith(fi, I, lambda x, y: y if x else -y)) for fi in F]

    # Reduce N rank matrix to N-dimensional vector with (+) operation
    [sum(i) for i in d]


# plt.hist(I)
# plt.title('Tier I')
# plt.show()
