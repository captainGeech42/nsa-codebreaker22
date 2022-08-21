#!/usr/bin/env python3

import base64
import binascii

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

# 0x20
salt = base64.b64decode("gvkAE1VsL/pMABtgLHr8+A6XpUqDs7tBnkcC4DWmaWA=")

# 0x40
secret = "pF6pU03MWGB2QH27nlfmxbV9K9fgIVI2Aao0QetBjLwOc9NO2/CJJnSfrcq62u4acbhs1HrfBkLqlu4qaSm82Q=="

ctxt = base64.b64decode("cTFwGnDr00p/8ODJuXOVKKNbuE9XcB6FrDZbYFl3nmNjoKFsza6u9NA2sKJslcQWA3Z36NVPysLlI7JCiCNKyQ==")
ptxt = b"22c18057-218d-11ed-af82-482ae328"

data = PBKDF2(secret, salt, 0x40, count=0x1000, hmac_hash_module=SHA256)
key = data[:0x20]
iv = data[0x20:]

print(f"key: {base64.b64encode(key).decode()}")
print(f"IV: {base64.b64encode(iv).decode()}")