# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 22:22:21 2020

@author: AsteriskAmpersand
"""


keys = [0xac76cb97ec7500133a81038e7a82c80a,#00
        0x6bb5c956e44d00bc305233cfbfaafa25,#01
        0x8f021dccb0f2787206fbdee2390bbb5c,#02
        0xda5c1e531d8359157875bd63bfaafa25,#03
        0x1f6d31c883dd716d7e8f598ce23f1929,#04
        0x4bb0de04e4e0856980ccb2942f9ce9f9,#05
        0x8bce54dc4c11139a7875bd63bfaafa25,#06
        0xec13345966ce7312440089a2ceddcee9,#07
        0xe4662c709c753a039a2c0f5ae23f1929,#08
        0xa492fc9033949c15a033ac223735cca7,#09
        0x25099c1f911a26e5ce9172f07a82c80a,#10
        0xd1d29d7446d4fdf1a033ac223735cca7,#11
        0x7eb268373b5d361ed6d313e2933c4dcb,#12
        0xa1c7d2ea661895ac7875bd63bfaafa25,#13
        0x82a43b2108797c6a440089a2ceddcee9,#14
        0x41d055b3dd6015167e8f598ce23f1929,#15
        ]
byteKeys = [key.to_bytes(16,byteorder="big") for key in keys]
keyIndices = {ix:k for ix,k in enumerate(keys)}

class byteKeylookup(dict):
    byteKeyIndices = {tuple(bk):ix for ix,bk in enumerate(byteKeys)}
    def __getitem__(self,value):
        return self.byteKeyIndices[tuple(value)]
byteKeyIndices = byteKeylookup()