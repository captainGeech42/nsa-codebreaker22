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

# 41345|CdmCLp3evVoJFVlDPZRraeDAxBj6u6Oue+47Oe2TM+QrHKJW5WXPXYDFLiufcV51OC6j0OY9k5lCuJxloz9xxQ==|4.352|TastelessHabitat|2021-06-09T08:16:14-04:00
# 17618|mOlk7hJ8VmX0EgX0/w3ZOQoO5p/RQKD38hdKO5pxUzfoMTNweplj+02E1wGAwqTuZ+8wTMEcex9OYNjt40UPSQ==|3.334|AncientAncestor|2021-07-31T09:37:07-04:00
enc_data = base64.b64decode("mOlk7hJ8VmX0EgX0/w3ZOQoO5p/RQKD38hdKO5pxUzfoMTNweplj+02E1wGAwqTuZ+8wTMEcex9OYNjt40UPSQ==")

data = PBKDF2(secret, salt, 0x20, count=0x1000, hmac_hash_module=SHA256)
key = data[:0x20]

print(f"key: {base64.b64encode(key).decode()}")

iv = enc_data[:0x10]
aes = AES.new(key, AES.MODE_CBC, iv)
print(unpad(aes.decrypt(enc_data[0x10:]), 0x10))