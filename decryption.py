# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:58:26 2020

@author: AsteriskAmpersand
"""
from Crypto.Cipher import Blowfish
import sys
import struct
import hashlib
from pathlib import Path
from itertools import zip_longest

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def endianness_reversal(data):
    return b''.join(map(lambda x: x[::-1],chunks(data, 4)))

def CapcomBlowfishDecrypt(file,key = b"xieZjoe#P2134-3zmaghgpqoe0z8$3azeq"):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    return bytearray(endianness_reversal(cipher.decrypt(endianness_reversal(file))))

def CapcomBlowfishEncrypt(file,key = b"xieZjoe#P2134-3zmaghgpqoe0z8$3azeq"):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    return endianness_reversal(cipher.encrypt(endianness_reversal(bytes(file))))

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

zeroBytes = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

decrypt = CapcomBlowfishDecrypt
encrypt = CapcomBlowfishEncrypt