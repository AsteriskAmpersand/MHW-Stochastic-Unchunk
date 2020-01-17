# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:44:44 2020

@author: AsteriskAmpersand
"""


from bunnieHopKeygen import keygen
from keys import byteKeys
from decryption import byte_xor
from pathlib import Path
import multiprocessing
from multiprocessing import Pool
from keyFileManager import KeyFile
threadCount = multiprocessing.cpu_count()
chunkPath = r"E:\Program Files (x86)\Steam\steamapps\common\Monster Hunter World\chunk\decmp"
chunkCount = 234736

def pathFromIx(ix):
    return r"%s\chunk_%08d_decmp.bin"%(chunkPath,ix)

def decryptedFromIx(ix):
    return r"%s\chunk_%08d_dcrpt.dbin"%(chunkPath,ix)

blockKeys = [bkey*0x4000 for bkey in byteKeys]
def blockXor(bkey,block):
    return byte_xor(bkey,block)

def xorDecrypt(bkey,block):
    return blockXor(bkey,block)

def generateKeyseq():
    genFunc = keygen()
    return [next(genFunc) for i in range(1,chunkCount)]

keyseq = generateKeyseq()

def writeKeyseq(outfpath):
    keyf = KeyFile(keys = keyseq)
    keyf.writeKeyFile(outfpath)
    
def readKeyseq(infpath):
    keys = KeyFile(keyFilePath=infpath)
    return keys.keys

def parallelDecrypt(ix):
    if not(ix%1000):
        print("Chunk: %06d/%06d"%(ix,chunkCount))
    pix = ix+1
    key = blockKeys[keyseq[ix]]
    with open(decryptedFromIx(pix),"wb") as outf:
        with open(pathFromIx(pix),"rb") as chonk:
                outf.write(xorDecrypt(key,chonk.read()))
    return True

def mergeDecrypted():
    with open("%s\chunkG0.pkg","wb"%chunkPath) as outf:
        for ix in range(1,chunkCount):
            with open(decryptedFromIx(ix),"rb") as inf:
                outf.write(inf.read())
                
def parallelUnencryptChunk():
    pool = Pool(processes=threadCount)
    pool.imap_unordered(parallelDecrypt,range(0,chunkCount-1))
    pool.close()
    pool.join()
    mergeDecrypted()
        
def unencryptChunk(outf):
    genFunc = keygen()
    for ix, keyIx in zip(range(1,chunkCount),genFunc):
        if not((ix-1)%1000):
            print("Chunk: %06d/%06d"%(ix,chunkCount))
        key = blockKeys[keyIx]
        with open(pathFromIx(ix),"rb") as chonk:
            outf.write(xorDecrypt(key,chonk.read()))

#with open("%s\chunkG0.pkg"%chunkPath,"wb") as outf:
#    unencryptChunk(outf)
if __name__ == "__main__":
    parallelUnencryptChunk()