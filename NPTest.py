__author__ = 'oyakov'

import numpy.matlib as ml

a = ml.mat([[1, 2, 3], [3, 2, 1], [1, 1, 1]])
b = ml.mat([[1, 2, 3], [3, 2, 1], [1, 1, 1]])
print(a + b)