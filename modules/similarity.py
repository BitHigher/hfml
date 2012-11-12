#!/usr/bin/python
from math import sqrt

def euclidean(v1, v2):
    '''
        v1 and v2 are two vectors of the same length.
        calculate the euclidean distance of v1 and v2,
        return 1 / (1 + distance), which define the 
        similarity of v1 and v2
    '''
    length = min(len(v1), len(v2))
    if length == 0: return 0
    
    d = 0
    for i in range(length):
        d += pow((v1[i] - v2[i]), 2)
    #return sqrt(d)
    return 1 / float(1+d)

def cosine(v1, v2):
    length = min(len(v1), len(v2))
    if length == 0: return 0
    
    dp = 0 #dot product
    m1 = 0 #modulus of v1
    m2 = 0 #modulus of v2
    for i in range(length):
        dp += v1[i] * v2[i]
        m1 += v1[i] * v1[i]
        m2 += v2[i] * v2[i]
    
    if m1 == 0 or m2 == 0: return 0
    distance = dp / (sqrt(m1) * sqrt(m2))
    return distance

def pearson(v1, v2):
    length = min(len(v1), len(v2))
    if length == 0: return 0
    
    #e of v1 v2
    e1 = 0
    e2 = 0
    for i in range(length):
        e1 += v1[i]
        e2 += v2[i]
    e1 /= float(length)
    e2 /= float(length)
    
    cov = 0 #cov of v1 v2
    d1 = 0 #variance of v2
    d2 = 0 #variance of v2
    for i in range(length):
        diff1 = v1[i] - e1
        diff2 = v2[i] - e2
        cov += diff1 * diff2
        d1 += diff1 * diff1
        d2 += diff2 * diff2
    cov /= float(length)
    d1 /= float(length)
    d2 /= float(length)
    
    if d1 == 0 or d2 == 0: return 0
    return cov / sqrt(d1 * d2)
