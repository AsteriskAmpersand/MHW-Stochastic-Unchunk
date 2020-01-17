# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 22:54:01 2020

@author: AsteriskAmpersand
"""
from keys import byteKeys, byteKeyIndices
from decryption import byte_xor, zeroBytes, grouper
import operator
from decryption import decrypt
from fileSignatures import FileSignatureManager
from itertools import cycle
from keyFileManager import KeyFile
from decryptChunk import pathFromIx, chunkCount
import multiprocessing
from multiprocessing import Pool
threadCount = multiprocessing.cpu_count()

def testSpeedDecrypt(bkey,block):
    for subblock in grouper(16, block):
        dec = byte_xor(bkey,subblock)
        if dec == zeroBytes:
            return True
    return False

def bruteForceSpeedDecrypt(block, bkeys = byteKeys):
    candidates = []
    for k,key in enumerate(bkeys):
        decrypts = testSpeedDecrypt(key,block)
        if decrypts:
            candidates.append(k)
    if len(candidates)>1:
        return -2
    if not candidates:
        return -1
    else:
        return candidates[0]
    
def testDecrypt(bkey,block):
    count = 0
    for subblock in grouper(16, block):
        dec = byte_xor(bkey,subblock)
        if dec == zeroBytes:
            count+=1
    return count

def bruteForceDecryptBlock(block,bkeys = byteKeys):
    keyZeros = {}
    for bkey in bkeys:
        score,data = testDecrypt(bkey,block)
        keyZeros[tuple(bkey)] = score
    bestKey = byteKeyIndices[max(keyZeros.items(), key=operator.itemgetter(1))[0]]
    return bestKey

def cycleKey(startPosition,key):
    return cycle(key[startPosition%16:]+key[:startPosition%16])

def snipeDecrypt(signature,cbkey,block, encryption):
    siglen = len(signature)
    if encryption:
        xorcypherdata = block[:16]
        cypherdata = byte_xor(cbkey,xorcypherdata)
        data = decrypt(cypherdata,encryption)
        if data[:siglen] == signature:
            return True
    else:
        sigcandidate = block[:siglen]
        if byte_xor(sigcandidate,cbkey) == signature:
            return True
    return False

def testSpeedInformedDecrypt(cbkey, block, encryption):
    for subblock in grouper(16, block):
        cypdec = byte_xor(cbkey,subblock)
        dec = decrypt(cypdec,encryption)
        if dec == zeroBytes:
            return True
    return False

def recalcFileSize(fileSizeInChunk, boffset):
    if fileSizeInChunk == 0x40000:
        return fileSizeInChunk-(0x10-boffset)*(boffset != 0)
    else:
        return fileSizeInChunk

fileSignatures = FileSignatureManager()
def analyzeData(fileData,block):
    isHeader, offset, encryption, signature, fileSizeInChunk = fileData
    candidates = set()
    for bkey in byteKeys:
        cbkey = cycleKey(offset%0x10,bkey)
        #not enough data to decrypt blowfish
        if not isHeader and encryption:
            if fileSizeInChunk < ((offset%0x10)+0x10):
                continue
        #not enough data to read sig
        if fileSizeInChunk < (0x10 if encryption else len(signature)):
            continue
        if isHeader:
            nblock = block[offset:offset+fileSizeInChunk]
            def test(*args):
                return snipeDecrypt(signature,*args)
        else:
            boffset = offset%0x10
            nblock = block[boffset:recalcFileSize(fileSizeInChunk,boffset)]
            test = testSpeedInformedDecrypt
        decrypts = test(cbkey, nblock)
        if decrypts:
            candidates.add(byteKeyIndices[bkey])
    return candidates

def informedDecrypt(block, blockIx):
    filesInChunk = fileSignatures[blockIx]
    candidates = set(byteKeys)
    for fileData in filesInChunk:
        candidatum = analyzeData(fileData,block)
        if candidatum:
            candidates.intersection(candidatum)
    if len(candidates)>1:
        return -2
    if not candidates:
        return -1
    else:
        return candidates[0]

knownKeys = KeyFile(keyFilePath = r"E:\MHW Ghetto Unchunk\data\mergedKeys.key")
theorizedKeys = KeyFile(keyFilePath = r"E:\MHW Ghetto Unchunk\data\keygen.key")
def parallelDecrypt(ix):
    if not(ix%1000):
        print("Chunk: %06d/%06d"%(ix,chunkCount))
    keygenKey = theorizedKeys[ix+1]
    knownKey = knownKeys[ix+1]
    #last known correct keygen 199672
    if knownKey < 0:
        blockf = open(pathFromIx(ix+1),"rb")
        block = blockf.read()
        blockf.close()
        knownKey = informedDecrypt(block,ix)
        knownKeys[ix+1] = knownKey
    if keygenKey != knownKey and knownKey >= 0:
        print("Keygen Mismatch %d/%d %d"%(keygenKey,knownKey,ix+1))
        raise ValueError
    
def decryptChunks():
    for i in range(0,chunkCount-1):
        parallelDecrypt(i)
    
def decryptChunksParallel():
    pool = Pool(processes=threadCount)
    pool.imap_unordered(parallelDecrypt,range(0 ,chunkCount-1))
    pool.close()
    pool.join()        
        
if __name__ == "__main__":
    decryptChunks()
    knownKeys.writeKeyFile(r"E:\MHW Ghetto Unchunk\data\KnownKeys.key")
    knownKeys.writeCsv(r"E:\MHW Ghetto Unchunk\data\KnownKeys.csv")
        
