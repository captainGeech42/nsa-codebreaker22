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
# aes = AES.new(base64.b64decode("ci/zCrpl6r8Sb99bMpc0X/6JqwzjspqGE7A/4jNgifc="), AES.MODE_CBC, ctxt[:0x10])
aes = AES.new(b"449fc6e6-d6b6-11", AES.MODE_CBC, iv)

ptxt = aes.decrypt(ctxt)
# ptxt = aes.decrypt(ctxt)

with open("test.pdf", "wb") as f:
    f.write(ptxt)