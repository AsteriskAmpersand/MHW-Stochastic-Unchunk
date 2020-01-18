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
    layers = [#-int(not(x % 3792)),
              #-int(not(x % 82107)),
              #not(x % 200539),
              ]
    return  sum(layers)

def rootPattern(ix):
    return (0, 0, 1, 0, 1)*ix + (0, 1)

def ljoin(head,seq):
    total = []
    for ele in seq:
        total += head+ele
    return total

def seqToRoot(seq):
    return ljoin(rootPattern(16),map(lambda x: x*rootPattern(15),seq))
    
basePattern = sum(map(seqToRoot,[(2,2,3)*3,(2,3,2)*3,(3,2,2)*3]),[])

def spacing(i):
    return [0]*(i-1) + [1]

nineteenNoise = spacing(19)*10 + spacing(20) + spacing(19)*9 + spacing(20)

class keygen():
    def __init__(self):
        self.ix = -1
        self.prev = 14
        self.pattern = cycle(basePattern)
        self.ninteenNoise = cycle(nineteenNoise)
        next(self.pattern)  
        self.noise = noiseLayer        
    
    def __next__(self):
        if self.ix == -1:
            self.ix = 0
            return 0
        if self.ix == 0:
            self.ix = 1
            return 1
        p = next(self.pattern)
        n = self.noise(self.ix)
        l = next(self.ninteenNoise)
        key, self.prev = keyStep(self.prev,p+n+l)
        self.ix+=1  
        return key
    def __iter__(self):
        return self
    def ammend(self,key):
        self.prev = key


def keygenChunk():
    chunkCount = 234736
    k = keygen()
    keys = [next(k) for i in range(1,chunkCount)]
    kf = KeyFile(keys = keys)
    return kf

if __name__ in "__main__":
    kf = keygenChunk()
    kf.writeKeyFile(r"E:\MHW Ghetto Unchunk\data\keygen.key")
    kf.writeCsv(r"E:\MHW Ghetto Unchunk\data\keygen.csv")
    
        
