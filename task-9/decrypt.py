#!/usr/bin/env python3

import subprocess
import base64
import binascii
import os

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
from tqdm import tqdm

with open("important_data.pdf.enc", "rb") as f:
    enc_data = f.read()

iv = binascii.unhexlify(enc_data[:0x20])
ctxt = enc_data[0x20:]
"""
$ go run . 2021-10-03T11:42:32-04:00
generating uuid for 2021-10-03T11:42:32-04:00
2021-10-03 11:42:32 -0400 EDT
low: 85afe400
mid: 2460
hi: 11ec
seq: 9e40
85afe400-2460-11ec-974f-3302a1510000
"""
tmpl = "8xxxxxxx-2460-11ec-974f-3302a151"
start_ts = 0x5afe400

max_delta = (10**9) // 100 # uuidv1 is 100ns percision

for i in tqdm(range(start_ts, start_ts+max_delta)):
    # example uuid: 83716abd-f2ed-11eb-974f-3302a151

    uuid = tmpl.replace("xxxxxxx", hex(i)[2:])

    key = uuid.encode()
    aes = AES.new(key, AES.MODE_CBC, iv)

    ptxt = aes.decrypt(ctxt)
    if ptxt[:4] == b"%PDF":
        print(f"decrypted with {key}")

        with open("important_data.pdf", "wb") as f:
            f.write(aes.decrypt(ctxt))

        break        