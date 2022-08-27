#!/usr/bin/env python3

import base64
import binascii

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad

# 0x20
salt = base64.b64decode("gvkAE1VsL/pMABtgLHr8+A6XpUqDs7tBnkcC4DWmaWA=")

# 0x40
secret = "pF6pU03MWGB2QH27nlfmxbV9K9fgIVI2Aao0QetBjLwOc9NO2/CJJnSfrcq62u4acbhs1HrfBkLqlu4qaSm82Q=="

data = PBKDF2(secret, salt, 0x20, count=0x1000, hmac_hash_module=SHA256)
key = data[:0x20]

with open("all_db_entries", "r") as f:
    lines = [x.strip() for x in f.readlines()]

for l in lines:
    enc_data = base64.b64decode(l)
    iv = enc_data[:0x10]
    if iv == binascii.unhexlify("ea349a5aa3e501e9a0b28a29f2e97558"):
        print("yes")
        print(l)
    ctxt = enc_data[0x10:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    print(unpad(aes.decrypt(ctxt), 0x10))