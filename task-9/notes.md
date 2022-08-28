```
$ xxd important_data.pdf.enc|head -10
00000000: 6561 3334 3961 3561 6133 6535 3031 6539  ea349a5aa3e501e9
00000010: 6130 6232 3861 3239 6632 6539 3735 3538  a0b28a29f2e97558
00000020: 5e5b 6ae3 a464 e900 2a20 290f 95e3 bb6f  ^[j..d..* )....o
00000030: df33 1f2f f690 fd61 fe30 2d34 8702 8fb3  .3./...a.0-4....
```

there are 50 rows in the database and 68 in the log

$ ./find_missing_db_entries.py
10
2021-01-14T23:58:05-0500,TriteBuddy,14139,5.758
2021-01-19T20:43:27-0500,TriteBuddy,48870,8.194
2021-02-26T07:59:33-0500,AberrantReboot,32610,3.901
2021-08-28T13:17:21-0400,TriteBuddy,46598,9.363
2021-09-23T04:27:31-0400,TastelessHabitat,12442,4.434
2021-10-03T11:42:32-0400,MelodicVixen,17033,8.539
2021-11-21T03:09:16-0500,AccessibleTinderbox,43175,2.524
2021-12-20T18:44:50-0500,ElegantCreative,36620,9.748
2021-12-26T00:59:34-0500,AncientAncestor,44017,6.879
2021-12-31T13:38:16-0500,TriteBuddy,20345,3.845


the one MelodicVixen line may be it?
    compute the UUID, use it to figure out what the AES key is, decrypt the file?
    idk

uuid is timestamp plus some fixed data
examples from decrypted db:
    83716abd-f2ed-11eb-974f-3302a151
    787ab34c-7832-11eb-974f-3302a151
    7db3d6f0-3d09-11ec-974f-3302a151
    659897b8-f204-11eb-974f-3302a151

get timestamp from the missing db entries, get uuid. uuid raw bytes are the key, leading 32hex is iv?

test uuid:
    657ed244-262f-11ed-90ce-482ae328
    ts: 2022-08-27T13:40:52-04:00

```
$ go run . 2022-08-27T13:40:52-04:00
generating uuid for 2022-08-27T13:40:52-04:00
2022-08-27 13:40:52 -0400 EDT
low: 651bea00
mid: 262f
hi: 11ed
seq: 8f7f
651bea00-262f-11ed-8f7f-000000000000
```

none of the keys in the database decrypt the pdf

the log has 2022 entries, the db does not

need a 5-13 second variance for each timestamp, ugh

https://gztkmtljeceezgmv.ransommethis.net/demand?cid=6158061
    dont think this is needed but jic

---------------

# binary capability

## lock

usage: `./keyMaster <customer id: int> <expected payment: float> <hacker name: str>`

example:
```
$ ./keyMaster lock 2 3 MelodicVixen
{"plainKey":"11ef29f4-2638-11ed-a575-482ae328","result":"ok"}
```

writes the following row to db:
```
2|hgwoskzEnqOgpo/9L5dPCtJs6jpqC2froBNDvwGwMNTmES7jdA+igt/sguOEamhFzI1B68vJNfMcdBe95gA9Jw==|3.0|MelodicVixen|2022-08-27T14:42:57-04:00
```

encrypted data in the database
    first 0x10 is IV, rest of ciphertext
    find_db_entry.py decrypts

$CLOCK_SEQUENCE is 0x974f

UUIDv1 time component is 100ns precision. we lose a lot of precision by using a timestamp from the log

* generate a uuidv1
  * clock sequence is 0x974f
  * nodeid is 0x3302a151

## unlock

usage:
```
$ ./keyMaster unlock <jwt>
{"key":"MjFmNGZlNDUtNTBjNS0xMWVjLTk3NGYtMzMwMmExNTE="}
```

outputs a base64 encoded key from the db i think?

read in a PEM RSA pubkey from ./receipt.pub
parse a jwt

Parser.ParseWithClaims call, va 0x5b8a52
    rax - Parser ptr
    rbx - tokenString.ptr
    rcx - tokenString.length
    rdi/rsi - ReceiptClaims, unsure on the values
    r8 - KeyFunc

at 0x599589, the standard claims are validated
```go
type StandardClaims struct {
	Audience  string `json:"aud,omitempty"`
	ExpiresAt int64  `json:"exp,omitempty"`
	Id        string `json:"jti,omitempty"`
	IssuedAt  int64  `json:"iat,omitempty"`
	Issuer    string `json:"iss,omitempty"`
	NotBefore int64  `json:"nbf,omitempty"`
	Subject   string `json:"sub,omitempty"`
}
```

after call at 0x5b8a52, a token pointer is in rax
```go
type Token struct {
	Raw       string                 // The raw token.  Populated when you Parse a token
	Method    SigningMethod          // The signing method used or to be used
	Header    map[string]interface{} // The first segment of the token
	Claims    Claims                 // The second segment of the token
	Signature string                 // The third segment of the token.  Populated when you Parse a token
	Valid     bool                   // Is the token valid?  Populated when you Parse/Verify a token
}
```

jwt: `eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b21lcklEIjoiMzQ5NjIiLCJwYXltZW50QW1vdW50Ijo2Ljl9.PVUZxrqxvjpLQnwIp05Ekco3w78JrSV1VEUlyPpL9Rpr-ScYK8apAjhqOSfMfBGMYeDWIt7zDIroxUd_X1eIA_C1YoB_DeGN9Lq2NFPrODdLUQWUk3IRXMrM0yZTqnspTN0ecOj21M4aUNf3NMuuBZqCl6wH6OHwxIU1WNxDf-xYXmvwV4XHFmx956CLRIiyEgljEY-CgeAH--QWHwmBcbu5jRLclMxNMyaZgto7ghEynRRTSA_0GoxaDKK-RNV5APFOTyATkweXmnpgELpRzcyv5omtxl08aK7cbjxo-SUvS-019uS6JvbS76XW_dXB7su_T0YzQH_-ePl2XikYRw`

claims:
```json
{
    "customerID": "34962",
    "paymentAmount": 6.9,
}
```

0x6B0AC0 has the struct definition for receipt claims



## credit

--------------------------------

```
#################### 2022-01-24T08:41:29-0500: decrypted with b'55964e7f-7d1b-11ec-974f-3302a151'

00001c00: f286 39cf 30e1 4698 d5f4 e0ac f3d8 a6cb  ..9.0.F.........
00001c10: 7a8c 3014 ae86 9837 e29c 1814 8fa1 44f5  z.0....7......D.
00001c20: acbb 507d 55e1 89b7 296d 2545 4f46 6d6f  ..P}U...)m%EOFmo
(END)
```

last two should be 0d 0a

#################### 2022-01-11T20:22:27-0500: decrypted with b'1a7ca462-7346-11ec-974f-3302a151'
    no clue why this came up

#################### 2022-01-11T20:22:33-0500: decrypted with b'1e3ab0d5-7346-11ec-974f-3302a151'
    %EOF at the very end

#################### 2022-02-11T18:50:05-0500: decrypted with b'56633d1a-8b95-11ec-974f-3302a151'