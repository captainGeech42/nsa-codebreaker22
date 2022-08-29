#!/usr/bin/env python3

import functools
from datetime import timedelta
import multiprocessing
import subprocess
import base64
import binascii
import os
import traceback

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
from tqdm import tqdm
from dateutil.parser import parse as dt_parse

print = functools.partial(print, flush=True)

with open("important_data.pdf.enc", "rb") as f:
    enc_data = f.read()

iv = binascii.unhexlify(enc_data[:0x20])
ctxt = enc_data[0x20:]

CLOCK_SEQUENCE_OFFSET = 0

TIMESTAMPS = [
    # "2022-01-02T23:25:14-0500",
    # "2022-01-11T20:22:38-0500",
    # "2022-01-15T15:19:11-0500",
    # "2022-01-22T17:27:11-0500",
    # "2022-01-24T08:41:42-0500",
    # "2022-02-11T18:50:18-0500",
    # "2022-02-16T09:45:09-0500",
    # "2022-02-20T05:31:12-0500",
    # "2022-02-23T04:11:52-0500",
    # "2022-03-12T16:02:07-0500",
    # "2022-04-15T03:09:16-0400",
    # "2022-05-11T16:03:22-0400",
    "2022-05-18T10:24:54-0400",
    # "2022-05-19T01:27:25-0400",
    # "2022-05-30T22:05:16-0400",
    # "2022-06-11T04:06:51-0400",
    # "2022-06-27T00:20:32-0400",
    # "2022-07-06T19:17:47-0400",
]

max_delta = (10**9) // 100 # uuidv1 is 100ns percision; 0x98_96_80

ALL_TIMESTAMPS = []

# in the records where we have log+db timestamps, the database timestamps are a few sec earlier than the log times
for ts in TIMESTAMPS:
    dt = dt_parse(ts)
    for i in range(5, 14):
        ALL_TIMESTAMPS.append((dt-timedelta(seconds=i)).strftime("%Y-%m-%dT%H:%M:%S%z"))

# ALL_TIMESTAMPS = ALL_TIMESTAMPS[:1]

def try_ts(ts):
    print(f"testing {ts}")

    uuid = subprocess.check_output(["./convert_ts_to_uuid", ts])
    start_key = uuid[:32].decode()

    # set clock sequence
    parts = start_key.split("-")
    clock_sequence = int(parts[3], 16)
    clock_sequence += CLOCK_SEQUENCE_OFFSET
    parts[3] = hex(clock_sequence)[2:]
    start_key = "-".join(parts)

    start_ts = int(start_key[:8], 16)
    tail = start_key[8:]

    # need to go backwards from the non-precise starting UUID
    for i in range(start_ts-max_delta, start_ts):
        uuid_key = (hex(i)[2:].zfill(8) + tail).encode()
        key = uuid_key[:0x10]

        try:
            aes = AES.new(key, AES.MODE_CBC, iv)
        except ValueError:
            print(f"exception while doing {ts}")
            traceback.print_exc()
            print(f"uuid: {uuid}")
            print(f"start_key: {start_key}")
            print(f"uuid_key: {uuid_key}")
            print(f"key: {key}")
            break

        ptxt = aes.decrypt(ctxt)
        # if ptxt[:4] == b"%PDF":
        if b"%PDF" in ptxt[:10] or b"%EOF" in ptxt[-10:]:
            print(f"#################### {ts}: possibly decrypted with {key}")

            with open(f"important_data_{key}.pdf", "wb") as f:
                f.write(ptxt)
    
    print(f"finished {ts}")

if __name__ == "__main__":
    with multiprocessing.Pool(40) as pool:
        pool.map(try_ts, ALL_TIMESTAMPS)