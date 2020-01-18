# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 17:22:13 2020

@author: AsteriskAmpersand
"""
from functools import partial
from pathlib import Path
import csv
import sys

class ListAsFile():
    def __init__(self,listing):
        self.innerlist = listing
        self.pointer = 0
    def read(self,x):
        data = self.innerlist[self.pointer:self.pointer+x]
        self.pointer +=x
        return data
    def close(self):
        return

class Interval():
    '''Clopen interval'''
    def __init__(self, start,end):
        self.start = start
        self.end = end
    def __contains__(self,val):
        return self.start <= val < self.end
    def __len__(self):
        return self.end - self.start
    
class KeyFile():
    def __init__(self,start = 1, keys = [], keyFilePath = r"", keyData = []):
        if keyFilePath == r"" and not keyData:
            end = start + len(keys)
            self.range = Interval(start,end)
            self.keys = keys
        else:
            if keyData:
                kf = ListAsFile(keyData)
            else:
                kf = open(keyFilePath,"rb")
            self.range, self.keys = self.readKeyFile(kf)            
            
    def __getitem__(self,ix):
        return self.keys[ix-self.range.start]    
    def __setitem__(self,ix,value):
        self.keys[ix-self.range.start] = value   
            
    @staticmethod
    def readKeyFile(keyFileData, access = "read"):        
        start = int.from_bytes(getattr(keyFileData,access)(4),"little")
        end = int.from_bytes(keyFileData.read(4),"little")
        indices = []
        for ix in iter(partial(getattr(keyFileData,access),1),b""):
            indices.append(int.from_bytes(ix,"little",signed = True))
        end = start + len(indices)
        return Interval(start,end),indices
    
    def writeKeyFile(self,keyFilePath):
        start,end = self.range.start, self.range.end
        with open(keyFilePath,"wb") as outfile:
            outfile.write(start.to_bytes(4,"little"))
            outfile.write(end.to_bytes(4,"little"))
            for key in self.keys:
                outfile.write(key.to_bytes(1,"little",signed = True))
        
    def writeCsv(self,keyFilePath):
        start = self.range.start
        with open(keyFilePath,"w") as outfile:
            for ix,key in enumerate(self.keys):
                outfile.write("%d,%d\n"%(ix+start-1,key))
        
    def insertRange(self,ranging,keys):
        l,r = ranging.start, ranging.end
        if l not in self.range:
            if l >= self.range.end:
                self.keys[self.range.end:l] = [-3]*(l-self.range.end)
                self.range.end = l
            if l < self.range.start:
                padding = [-3]*(r-self.range.start) if r < self.range.start else []
                self.keys[:0] = (keys+padding)[0:self.range.start-l]
                self.range.start,l = l,self.range.start
        if r-1 not in self.range:
            self.keys[self.range.end:r] = keys[self.range.end-l:r-l]
            self.range.end,r = r,self.range.end
        for i in range(l,r):
            self.updateKey(keys[i-ranging.start],i-self.range.start)

    def updateKey(self,newkey,index):
        #-1 No Key
        #-2 Too Many Keys
        #-3 404 File Not Found
        if newkey == -3:
            return
        oldkey = self.keys[index]        
        if newkey < 0:
            if oldkey >= 0:
                return
            else:
                if newkey == -1:
                    if oldkey == -2:
                        return
        else:
            if oldkey>0:
                if oldkey != newkey:
                    print(index)
                    print(oldkey)
                    print(newkey)
                    raise ValueError
        self.keys[index] = newkey
    
    def append(self,keyList):
        return self.insertRange(keyList.range, keyList.keys)

class KeyifyList(object):
    def __init__(self, inner, key):
        self.inner = inner
        self.key = key

    def __len__(self):
        return len(self.inner)

    def __getitem__(self, k):
        return self.key(self.inner[k])
    
def keyFromCsv(csvFilePath):
    with open(csvFilePath,"r") as csvFile:
        reader = csv.reader(csvFile)
        start, okey = next(reader)
        keys = [int(okey)]+[int(keying) for ix,keying in reader]
        start = int(start) + 1
        kf = KeyFile(start,keys)
        return kf
    
def csvToKey(csvFilePath):
    kf = keyFromCsv(csvFilePath)
    kf.writeKeyFile(csvFilePath.with_suffix(".key"))
    
def keyToCsv(keyFilePath):
    kf = KeyFile(keyFilePath = keyFilePath)
    kf.writeCsv(keyFilePath.with_suffix(".csv"))
    
if __name__ == "__main__":
    #sys.argv.append(r"E:\MHW Ghetto Unchunk\Tests\KnownKeys.key")
    if not (len(sys.argv)<2):
        conversionFile = Path(sys.argv[1])
        if conversionFile.suffix in [".key"]:
            keyToCsv(conversionFile)
        else:
            csvToKey(conversionFile)
    