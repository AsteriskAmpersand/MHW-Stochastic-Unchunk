# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 18:06:51 2020

@author: AsteriskAmpersand
"""
import csv
from pathlib import Path

signaturePath = r'E:\MHW Ghetto Unchunk\data\signatures.csv'
fileOffsetPath = r'E:\MHW Ghetto Unchunk\data\ChunkInfo-chunkG0.csv'

def readStringBytes(stringBytes):
    try:
        return bytearray(map(lambda x: int(x,16),stringBytes.split(" ")))
    except:
        return False

def loadKnownSignatures():
    knownExtensions = {}
    with open(signaturePath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)    
        for row in csvreader:
            data = {h:r for h,r in zip(header,row)}
            if data["Signature"] != '':
                if data["Encrypted"]=="TRUE" and not data["Key"]:
                    continue
                knownExtensions["."+data["Format"]]=(readStringBytes(data["Signature"]),bytes(data["Key"]))
    return knownExtensions

class FileData():
    signatures = loadKnownSignatures()
    def __init__(self,address,extension,localindex,localoffset,localsize,isHeader):
        self.address = address
        self.extension = extension
        self.offsetInOriginalChunk = localoffset
        self.chunkIndex = localindex
        self.sizeInChunk = localsize
        self.isHeader = isHeader
        self.encrypted = self.signatures[self.extension][1]
        self.signature = self.signatures[self.extension][0]
    def decompose(self):
        return (self.isHeader, self.offsetInOriginalChunk, 
                self.encrypted, self.signature, self.sizeInChunk)

class FileSignatureManager():
    signatures = loadKnownSignatures()
    def __init__(self, dataPath = fileOffsetPath):
        self.loadFileData(dataPath)
    
    def loadFileData(self, dataPath):
        total = []
        with open(dataPath, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)    
            for row in csvreader:
                data = {h:r for h,r in zip(header,row)}
                data["Extension"] = Path(data["FileAddress"]).suffix
                if data["Extension"] in self.signatures:
                    total += self.createDataEntry(data)                
        self.data = sorted(total,key = lambda x: x.chunkIndex)
        self.dataLookups = {}
        for entry in self.data:
            if entry.chunkIndex not in self.dataLookups:
                self.dataLookups = []
            self.dataLookups.append(entry)
                
    def createDataEntries(dataDic):
        address = dataDic["FileAddress"]
        extension = dataDic["Extension"]
        currentChunk = dataDic["ChunkIndex"]
        baseOffset = dataDic["OffsetInSingleChunk"]
        currentOffset = dataDic["OffsetInSingleChunk"]
        sizeLeft = dataDic["FileSize(B)"]
        header = True
        dataEntries = []
        while sizeLeft:
            localSize = min(0x40000-currentOffset, sizeLeft)
            dataEntries.append(FileData(address,extension,currentChunk,baseOffset, localSize, header))
            header = False
            sizeLeft = max(0,sizeLeft-localSize)
            currentOffset = 0
            currentChunk += 1
        return dataEntries
    
    def __get__(self,chunkindex):
        if chunkindex in self.dataLookups:
            return map(lambda x: x.decompose(), self.dataLookups[chunkindex])
        else:
            return []
    
#Path(data["FileAddress"]).suffix.replace(".","")
#isHeader, offset, encryption, signature, fileSizeInChunk = fileData