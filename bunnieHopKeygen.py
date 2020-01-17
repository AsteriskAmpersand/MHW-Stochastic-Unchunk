# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:35:08 2020

@author: AsteriskAmpersand
"""
from itertools import cycle
from keyFileManager import KeyFile

bunnieHops = [0, 7, 2, 3, 12, 8, 9, 4, 5, 15, 10, 14, 6, 13, 1, 11] 

def keyStep(prev, step):
    stepSize = [4,1,14]
    new = (prev+stepSize[step])%len(bunnieHops)
    return bunnieHops[new],new

def noiseLayer(x):
    """Plus to the step"""
    layers = [not((x - (x//200)) % 19),
              -int(not(x % 3792)),
              -int(not(x % 82107)),
              not(x % 200539),
              ]
    return  sum(layers)

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

def keygenChunk():
    chunkCount = 234736
    k = keygen()
    keys = [next(k) for i in range(1,chunkCount)]
    kf = KeyFile(keys = keys)
    return kf

if __name__ in "__main__":
    kf = keygenChunk()
    kf.writeKeyFile(r"E:\MHW Ghetto Unchunk\data\keygen.key")
    
        
