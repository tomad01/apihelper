from collections import defaultdict
from itertools import compress
try:
     from apihelper.file_analysis import *
except:
     from file_analysis import *
import numpy as np
import pdb
from dateutil.parser import parse

tests = [
    # (Type, Test)
    (int, int),
    (float, float),
    (datetime, lambda value: parse(value))
]

def getType(value):
     for typ, test in tests:
         try:
             test(value)
             return typ
         except ValueError:
             continue
     # No match
     return str

def substract(a,b):
    return [i - j for i, j in zip(a, b)]      

def show_first_n(a,n):
    return sorted(a.iteritems(), key=lambda x: x[1],reverse=True)[0:n]

def hist(a):
    d = defaultdict(int)
    for i in a:
      d[i] += 1
    return sorted(d.iteritems(), key=lambda x: x[1],reverse=True)

def mode(a):
    d = defaultdict(int)
    for i in a:
        d[i] += 1          
    return sorted(d.items(), key=lambda x: x[1])[-1][0]

def extract_mode(matrix):
    result = []
    for ii in range(len(matrix[0])):
        foo = matrix[:,ii]            
        result.append(mode(foo[foo != ''].astype(np.float)))
    return result

def extract_median(matrix):
    result = []
    for ii in range(len(matrix[0])):
        foo = matrix[:,ii]            
        result.append(np.median(foo[foo != ''].astype(np.float)))
    return result

def extract_mean(matrix):
    result = []
    for ii in range(len(matrix[0])):
        foo = matrix[:,ii]            
        result.append(np.mean(foo[foo != ''].astype(np.float)))
    return result

def comp_discret(ref,comp):
    '''this function returns two outputs:
    the likelihood coeficient between the input vectors
    calculated as the nr of elements from ref vec that also exists in comp vect divided by ref length
    and the balance coeficient calculated as the ratio between ref length and comp length'''
    return len([ '' for ii in ref if ii in comp])/float(len(ref)),len(ref)/float(len(comp))

def mad_based_outlier(points, thresh=3.5):
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
        
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(list(diff))
    med_abs_deviation = np.median(diff)
    if med_abs_deviation==0:
         return np.array([True]*len(points))
    modified_z_score = 0.6745 * diff / med_abs_deviation
    return modified_z_score < thresh

def rem_outliers_simp(vec):
    filt = mad_based_outlier(vec)
    return np.array(list(compress(vec, filt)))

def rem_outliers(vec):
    ind = [ii for ii,jj in enumerate(vec)]
    filt = mad_based_outlier(vec.astype(np.float))
    return list(compress(vec, filt)),list(compress(ind, filt))
    
if __name__=="__main__":
##    from random import randint
##    data = [randint(1,9) for _ in range(10000)]+[1000,888,4444444,20]
####    data = [0.1,0.3,0.4,0.5,0.5,5,1000,8]
####    data = [1,3,4,0.5,5,1000,40,6,7,8,9,91]
##    print len(data)
##    f1 = reject_outliers(np.array(data))
##    f3 = percentile_based_outlier(np.array(data))
##    f4 = mad_based_outlier(np.array(data))
##    print len(f1)
##    print list(f3).count(False)
##    print list(f4).count(False)

    ref = [1,2,3,4,5]
    comp = [1,7,8,9,10]
##    print comp_discret(ref,comp)
