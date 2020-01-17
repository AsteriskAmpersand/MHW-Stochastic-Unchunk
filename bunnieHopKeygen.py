# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:35:08 2020

@author: AsteriskAmpersand
"""
from itertools import cycle

bunnieHops = [0, 7, 2, 3, 12, 8, 9, 4, 5, 15, 10, 14, 6, 13, 1, 11] 

def keyStep(prev, step):
    stepSize = [4,1,14]
    new = (prev+stepSize[step])%len(bunnieHops)
    return bunnieHops[new],new

def noiseLayer(center):
    """Plus to the step"""
    return  not((center - (center//200)) % 19)

basePattern =   (0, 0, 1, 0, 1)*16 + (0, 1)+\
                (0, 0, 1, 0, 1)*15 + (0, 1)+\
                (0, 0, 1, 0, 1)*15 + (0, 1)+\
                (0, 0, 1, 0, 1)*16 + (0, 1)+\
                (0, 0, 1, 0, 1)*15 + (0, 1)+\
                (0, 0, 1, 0, 1)*15 + (0, 1)+\
                (0, 0, 1, 0, 1)*16 + (0, 1)+\
                (0, 0, 1, 0, 1)*15 + (0, 1)+\
                (0, 0, 1, 0, 1)*15 + (0, 1)+\
                (0, 0, 1, 0, 1)*15 + (0, 1)

def keyEngine():
    ix = 1
    prev = 14
    pattern = cycle(basePattern)
    next(pattern)    
    noise = noiseLayer
    while True:
        key, prev = keyStep(prev,next(pattern) + noise(ix))
        ix+=1        
        yield key
    
def keygen():
    engine = keyEngine()
    yield 0
    yield 1
    while True:
        yield next(engine)
        
k = keygen()
for i in range(25):
    next(k)