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
        
        self.p = 0
        self.n = 0
        self.l = 1
    
    def __next__(self):
        if self.ix == -1:
            self.anterior = -1
            self.ix = 0
            return 0
        if self.ix == 0:
            self.anterior = 0
            self.ix = 1
            return 1
        self.p = next(self.pattern)
        self.n = self.noise(self.ix)
        self.l = next(self.ninteenNoise)
        self.anterior = self.prev
        key, self.prev = keyStep(self.prev,self.p+self.n+self.l)
        self.ix+=1  
        return key
    def __iter__(self):
        return self
    def ammend(self,key):
        self.prev = key
    def __repr__(self):
        return "Key %02d | Pattern %d | 19/20 Noise %d"%(bunnieHops[self.anterior],self.p,self.l)

def outputKeygenStates():
    g = keygen()
    next(g)
    with open(r"E:\MHW Ghetto Unchunk\data\keygenStates.txt","w") as outfile:
        for _ in range(240000):
            outfile.write(str(g)+"\n")
            next(g)

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
    
        
