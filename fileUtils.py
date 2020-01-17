# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 13:26:56 2020

@author: AsteriskAmpersand
"""
from itertools import zip_longest
from collections import OrderedDict
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import copy
logfile = open(r"E:\IceborneData\log (1).txt","r")
#logfile = open(r"E:\IceborneData\log_sorted_fileorder.txt","r")
#logfile = open(r"E:\IceborneData\log_withdatakeys.txt","r")
keyset = OrderedDict()
keylist = OrderedDict()
iterationScheme = []
for ix,line in enumerate(logfile):
    if line not in keyset:
        keyset[line]=[]
        keylist[line]=len(keylist)
    keyset[line].append(ix)
    iterationScheme.append(keylist[line])

def recursiveDif(keyIndices):
    return [r-l for l,r in zip(keyIndices[:-1],keyIndices[1:])]

distanceSet = set()
for key in keyset:
    if len(keyset[key])>2:
        for dist in recursiveDif(keyset[key]):
            distanceSet.add(dist)
        #print(list(map(lambda x: "%02d"%x,recursiveDif(keyset[key])))[:20])
#print (distanceSet)

def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

for group in grouper(16,iterationScheme):
    print(group)
#raise ValueError
#print(iterationScheme[:])

def bitlifyBlock(intlist):
    return ''.join([ bin(l)[2:].zfill(4) for l in intlist])

from collections import Counter
def frequencyAnalysis(iterationScheme):
    fig = plt.figure()
    ax = plt.axes(xlim=(-.75, 15.75), ylim=(0, 2))
    #line, = ax.plot([], [], lw=2)
    barcollection = plt.bar(range(16),[0]*16)
    def animate(i):
        k = Counter(iterationScheme[:i])
        y = [k[j] for j in range(16)] 
        ax.set_ylim(0, max(y)+2)
        for yval, b in zip(y,barcollection):
            b.set_height(yval)
            
    anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=len(iterationScheme),
                                 interval=100)
    anim.save('mymovie.gif',writer="imagemagick",fps=60)
    anim

    #anim.show()
    


def berlekamp_massey_algorithm(intData):
    """
    An implementation of the Berlekamp Massey Algorithm. Taken from Wikipedia [1]
    [1] - https://en.wikipedia.org/wiki/Berlekamp-Massey_algorithm
    The Berlekamp–Massey algorithm is an algorithm that will find the shortest linear feedback shift register (LFSR)
    for a given binary output sequence. The algorithm will also find the minimal polynomial of a linearly recurrent
    sequence in an arbitrary field. The field requirement means that the Berlekamp–Massey algorithm requires all
    non-zero elements to have a multiplicative inverse.
    :param block_data:
    :return:
    """
    block_data = bitlifyBlock(intData)
    n = len(block_data)
    c = np.zeros(n)
    b = np.zeros(n)
    c[0], b[0] = 1, 1
    l, m, i = 0, -1, 0
    int_data = [int(el) for el in block_data]
    while i < n:
        v = int_data[(i - l):i]
        v = v[::-1]
        cc = c[1:l + 1]
        d = (int_data[i] + np.dot(v, cc)) % 2
        if d == 1:
            temp = copy.copy(c)
            p = np.zeros(n)
            for j in range(0, l):
                if b[j] == 1:
                    p[j + i - m] = 1
            c = (c + p) % 2
            if l <= 0.5 * i:
                l = i + 1 - l
                m = i
                b = temp
        i += 1
    return l
#print(frequencyAnalysis(iterationScheme))
#berlekamp_massey_algorithm(iterationScheme[:iterationScheme.index(16)])