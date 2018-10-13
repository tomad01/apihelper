from file_analysis import *
from data_analysis import *
from timeit import timeit
from random import randint
import numpy as np


data = [randint(1,9) for _ in range(100000)]
print timeit('hist(data)',setup='from __main__ import hist,data',number=10)
print timeit('set(data)',setup='from __main__ import data',number=10)

