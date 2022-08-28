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
key = b'56633d1a-8b95-11ec-974f-3302a151'
aes = AES.new(key, AES.MODE_CBC, iv)

ptxt = aes.decrypt(ctxt)
print(f"decrypted with {key}")

with open("test.pdf", "wb") as f:
    f.write(aes.decrypt(ctxt))