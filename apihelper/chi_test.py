from __future__ import division
from collections import defaultdict
import numpy as np
import pdb
import scipy.stats as stats





test_table = {
    'attr1':['small','big','small','medium','medium','big','small','big','big','small','medium','small','big'],
##    'attr2':['smal','bi','smal','mediu','mediu','bi','smal','bi','bi','smal','mediu','smal','bi']
    'attr2':['no','no','no','no','no','no','yes','yes','yes','yes','yes','yes','yes']
##    'attr2':['no']*12+['yes']
    }


    


def chi_squared_test(test_table,col_pr,col_sec):
    #build test table
    def hist(a):
        d = defaultdict(int)
        for i in a:
          d[i] += 1
        return d

    help_table = {}
    for key in test_table:
        help_table[key] = hist(test_table[key])
        
    # degrees of freedom
    df = (len(help_table[col_pr].keys())-1)*(len(help_table[col_sec].keys())-1)
    
    # create dictionary
    work_table = {col_pr:{kk:defaultdict(int) for kk in help_table[col_pr].keys()}}
    
    # count
    length = len(test_table[test_table.keys()[0]])
    for ii in range(length):
        work_table[col_pr][test_table[col_pr][ii]][test_table[col_sec][ii]]+=1
    
    # expected
    numi = len(help_table[col_pr].keys())
    for kk in help_table[col_sec]:
        help_table[col_sec][kk] = help_table[col_sec][kk]/numi

    # chi square
    chi_squared_stat = 0
    for k1 in work_table[col_pr].keys():                    
        for k2 in work_table[col_pr][k1].keys():            
            chi_squared_stat += ((work_table[col_pr][k1][k2] - help_table[col_sec][k2])**2)/help_table[col_sec][k2]

    print("Chi square stat")
    print(chi_squared_stat)
    crit = stats.chi2.ppf(q = 0.95,df = df)
    print("Critical value")
    print(crit)
    p_value = 1 - stats.chi2.cdf(x=chi_squared_stat,df=df)
    print("P value")
    print(p_value)
    print('Degrees of freedom:')
    print(df)
        



if __name__=="__main__":
    chi_squared_test(test_table,'attr1','attr2')
