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

TIMESTAMPS = [
    "2022-01-02T23:25:14-05:00",
    "2022-01-11T20:22:38-05:00",
    "2022-01-15T15:19:11-05:00",
    "2022-01-22T17:27:11-05:00",
    "2022-01-24T08:41:42-05:00",
    # "2022-02-11T18:50:18-05:00",
    "2022-02-16T09:45:09-05:00",
    "2022-02-20T05:31:12-05:00",
    "2022-02-23T04:11:52-05:00",
    "2022-03-12T16:02:07-05:00",
    "2022-04-15T03:09:16-04:00",
    "2022-05-11T16:03:22-04:00",
    # "2022-05-18T10:24:54-04:00",
    "2022-05-19T01:27:25-04:00",
    "2022-05-30T22:05:16-04:00",
    "2022-06-11T04:06:51-04:00",
    "2022-06-27T00:20:32-04:00",
    "2022-07-06T19:17:47-04:00",
]

max_delta = (10**9) // 100 # uuidv1 is 100ns percision; 0x98_96_80

for ts in TIMESTAMPS:
    print(f"testing {ts}")

    uuid = subprocess.check_output(["./convert_ts_to_uuid", ts])
    start_key = uuid[:32].decode()
    start_ts = int(start_key[:8], 16)
    tail = start_key[8:]

    for i in tqdm(range(start_ts, start_ts+max_delta)):
        uuid = hex(i)[2:] + tail

        key = uuid.encode()
        aes = AES.new(key, AES.MODE_CBC, iv)

        ptxt = aes.decrypt(ctxt)
        if ptxt[:4] == b"%PDF":
            print(f"decrypted with {key}")

            with open("important_data.pdf", "wb") as f:
                f.write(aes.decrypt(ctxt))

            break        