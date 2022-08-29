```
$ xxd important_data.pdf.enc|head -10
00000000: 6561 3334 3961 3561 6133 6535 3031 6539  ea349a5aa3e501e9
00000010: 6130 6232 3861 3239 6632 6539 3735 3538  a0b28a29f2e97558
00000020: 5e5b 6ae3 a464 e900 2a20 290f 95e3 bb6f  ^[j..d..* )....o
00000030: df33 1f2f f690 fd61 fe30 2d34 8702 8fb3  .3./...a.0-4....
```

there are 50 rows in the database and 68 in the log, missing 2022 entries in the db

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
    decrypt_db_entry.py decrypts

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

outputs a base64 encoded key from the db

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

usage:
```
$ ./keyMaster credit MelodicVixen 420 <jwt>
{"result":"ok"}
```

i think the jwt is used to authenticate? since the signature is validated

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

maybe i have to pbkdf2
the key from unlock is base64 encoded. the pbkdf2 secret is base64 encoded when it is passed into pbkdf2, but the salt is b64 decoded.
    is the 32 hex chars in the file the pbkdf2 salt, the iv, both?

------------------------------------

# looking at the other data from the website

victims.db

```
sqlite> select cid, pAmount, datetime(dueDate, 'unixepoch') from Victims order by dueDate;
4971120|6.6|2022-01-02 17:26:09
3853425|1.846|2022-01-04 21:59:15
6808974|3.355|2022-01-05 05:50:39
2709178|1.274|2022-01-13 11:43:38
2976552|7.196|2022-01-16 17:40:26
9842069|3.091|2022-01-17 00:35:47
8252443|7.651|2022-01-20 07:31:29
1383185|4.161|2022-01-26 05:59:01
2618791|6.765|2022-02-02 07:43:51
8729068|9.562|2022-02-05 11:54:41
5608425|1.22|2022-02-06 15:35:49
8645549|2.212|2022-02-08 12:35:25
3562040|2.192|2022-02-12 03:19:04
4392734|5.149|2022-02-12 19:02:10
4119032|5.637|2022-02-17 10:47:56
9116133|0.644|2022-02-18 01:43:06
6158061|2.497|2022-02-20 21:35:33
6004159|8.75|2022-03-03 07:34:32
2273054|1.284|2022-03-04 06:30:46
3861877|2.899|2022-03-05 16:07:15
1215567|0.007|2022-03-06 16:55:29
8425097|5.978|2022-03-10 04:46:02
5149521|1.266|2022-03-15 16:15:52
2399669|3.404|2022-03-15 21:50:30
5752874|8.397|2022-03-16 08:11:51
1094758|7.712|2022-03-22 21:34:20
2713981|1.6|2022-03-28 12:07:40
6294145|1.551|2022-04-01 01:05:57
7711349|1.833|2022-04-01 23:53:14
5659364|6.396|2022-04-03 15:16:35
5850043|2.997|2022-04-14 02:05:58
6194274|2.231|2022-04-15 19:00:49
6158828|4.183|2022-04-20 20:25:46
9779382|8.575|2022-04-28 04:44:42
4653819|4.864|2022-05-05 21:48:13
5447006|0.852|2022-05-09 03:23:37
4437293|9.774|2022-05-10 03:02:03
3258287|1.97|2022-05-14 23:48:57
3390492|6.938|2022-05-23 15:24:24
3296907|1.894|2022-05-24 00:47:35
4500980|9.278|2022-05-26 04:01:42
5719905|7.156|2022-05-26 09:55:34
6381209|4.173|2022-05-27 20:45:21
2684848|2.692|2022-05-31 08:23:18
9827504|8.087|2022-06-01 03:39:27
2796942|1.733|2022-06-02 07:52:49
8096331|7.337|2022-06-07 03:37:44
4718210|8.457|2022-06-09 14:00:17
9189779|8.679|2022-06-09 21:30:34
5135601|1.117|2022-06-16 02:13:48
13692|1.066|2022-06-17 14:29:39
3015646|1.482|2022-06-21 01:22:26
5224389|4.012|2022-06-27 03:58:01
9968864|5.332|2022-06-28 17:21:41
```

user db

```
$ sqlite3 user.db 
SQLite version 3.39.2 2022-07-21 15:24:47
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE Accounts (userName TEXT, uid INTEGER, secret TEXT, isAdmin INTEGER, pwhash TEXT, pwsalt TEXT);
CREATE TABLE UserInfo (uid INTEGER, memberSince INTEGER, clientsHelped INTEGER, hackersHelped INTEGER, programsContributed INTEGER);
sqlite> select * from Accounts;
MelodicVixen|25761|P5QQulqB5WeBuSoXNxPlBsqtDesIdjqC|0|jBZOHtPFMrZv9mB+00xN+YEAM1RWk7iMQmMMcb8aDgHLzk/szJ2CMFD0TLQmRubc6NES4fDR0yqNYZqE56n2BA==|duVPdd7L7xs9IhCfhLiIRA
AccessibleTinderbox|2187|aYGiCMKZc19HyuImYY7Bll5MWNwBe3bH|1|Lr6XslOi9lzjgNYeufw3yxIaeCtgniTuMrCU4sw/3RjYFI2vYaThUUPbJkx3CgBQSwz/8c+D/VtgZX3yBLcdew==|gt0TzSOVfhUYkmbrmDjYsg
SulkyDryer|29555|cSYLP0Lqn8kDUhvodMVVHnFLLQZgZcyr|0|X1nPcZxkGvgolNjostNp6s7Xt2ZUBj/qlGaSqE7ahekfSMNCMMFd70IwvzaqUECB8lpiNhLD1Xv60sQhmQ8I/A==|hO8NrhgxHHe7v9rLf4ZHCw
ElegantCreative|49674|0h5SdlqkxsxC8f3RBLbfdp5b6Btt9FpV|0|1kpgvSMV4/+1/3sLaK/nOuLdWUubDRSc214MdvqFknHfjMTl0zwzKewPREA5OTpVSYeQ1VaQu1rgA002T7csQw==|qNKvvrhk9CtcbIgR3I4RxA
ExpensivePoultry|34818|4swH2t2UkhW9XYabEkT88X37rlCLlZPl|0|qNoxKOKGf9RmcvkO2pI6KVl6dGtUEeHAZn9ciLNxkh3tbirRBzJF8g/9xuxlgKZGLz2Ui41BOoTNGe8uEaWRtg==|S7fGGDLqwzUjPpwOl9Ms3A
KaputStreet|24581|uuY4smjuXvo5bCOpFMJvinLg897cGTuq|0|2PirWH0n+UFKfDmTGEUihVwhi6nTMIGxKFmW8LlokpXnxdV7GI0gmvQNORVQ4dEIpw8iUJsJ4McD2ZSYKAwUtg==|QX8WCS4uwRyrrH6xFFY8kg
AncientAncestor|16244|uKURFvYU60FT7mJzjVhPEQvkoVMSsMDI|0|tKVtEqGanA3hjzW+Ex6WmwdROOcinEVr+8AIW2uSLpAc+kCIozAA0X+oiBx9DEcAeyFsNq1yBbTwkFUiLj9CmQ==|HinkyKX14pK1SNd0QvMetQ
TriteBuddy|30090|b21ue14DLst0HX1RiUNu8Q0JkuKjI8A4|0|VHlezBdgWresREwNSinMxQ9eIpUcxqpgpaJDhZRivDQAuaIWM9B1jD6zpjLGtiPNrHj2CV6orfj1xKSr46v25g==|UDzAx_E7UufQe9LF-TUBOw
ThirstyChuck|49694|bpcsZnjxTMvqTfPIckToCwDqWQAcxJ5r|0|8ADx20Rj3TdScObK/7bqyVRpBLvbK5onoxEEsVC7uOc8c1rMm053ETNcN0Sp7SBg/qqTXJavTKk4PmxeYHglUw==|E74tG8oS70lV8ZeOS3QwxQ
DirefulKazoo|17553|iRV9hycoOLBhqg5pC7fnHb8ITeyk7LsQ|0|lwl52O992w+tyGf8kxD9i6gUEunWh/pkAC8oWp17/rTCz5pfyMJNHuRiNLn3EAS50OaPt61wcFtKdHX0LzI5tA==|dZRqHgmHQK3jfICfI6_ifQ
LowAntling|41097|7aTt8Jyt4DoryOF47ihG1LqfxqB2zbkx|0|I6X++NQcfoO8yi4abHD+QMtqNr/xhM2PEQ72gUUZheiDF9E5Ur1cMDZbO10OSA2EZj9ntgPcJNAIRdXcwtj+lg==|LIsYayoAmBBgcnkgzLCo3Q
AbackColt|19841|5mkvStKDfEgxolAIDxqRrglIq1yVMGJE|0|36+rXHFC/jVKl7TFvW4sLWGE6I0lFe0TQj2tMkVdRIMQHPRXK09s9ArAaf662FjPqx7dv9KK2h3mZLuZasCYcQ==|1xcE7Vg1ZgkryT6-v-WiuA
PlausibleEthyl|26915|vkJr6FlsN9h29Ytv18vz8tx5EgVtgGNe|0|EnsrOvUjvDobQ+epK6oGayvevjU70jIomHl4E1KaQAyByqShoRPSaKHBqyXxb5gK4fA2pwKzkaWbMQ92ysso9Q==|usaI2il6ytnWvslo5-vm-w
AberrantReboot|12573|OakfB4cgfGow4NIH06BpvgMm9dCK8ebS|0|t1S1/sOLXEmqtaGrk0ozwtcROu0PcqezLZDGWsTWIvcCQhbqyIFLlGR3LLKTyNpY4VWssuTFyH+pWMDKulbsiw==|hqQhNfiR5nvUyu2fwNUiJg
TastelessHabitat|33671|KyBi7lU45CDDmmU6Sun2GpXyW02w2WSm|0|GaJSeWRlazqLwm5BmBz92ACsFRTz6kHZFDbsz0wB8mJfxhxrw3jVQsx7bN5OCv91g0d4AZD5wkw9PqlbRnWxtA==|nH_L75oHwtM56gRGzQ3LaA
sqlite> select * from UserInfo;
25761|1614285042|15|8|15
2187|1636057842|23|13|12
29555|1644265842|5|8|12
49674|1592857842|25|10|24
34818|1596141043|27|28|5
24581|1588365043|16|7|26
16244|1602966643|14|19|3
30090|1629318643|21|6|11
49694|1604349043|10|24|3
17553|1638649843|9|24|1
41097|1585168243|4|9|14
19841|1604003443|18|17|14
26915|1595017843|12|21|25
12573|1582317043|17|21|12
33671|1635366643|5|8|9
```

keymaster db

```
sqlite> .schema
CREATE TABLE customers (customerId INTEGER, encryptedKey TEXT, expectedPayment REAL, hackerName TEXT, creationDate TEXT);
CREATE TABLE hackers (hackerName TEXT, credits INTEGER);
sqlite> select * from customers;
41345|CdmCLp3evVoJFVlDPZRraeDAxBj6u6Oue+47Oe2TM+QrHKJW5WXPXYDFLiufcV51OC6j0OY9k5lCuJxloz9xxQ==|4.352|TastelessHabitat|2021-06-09T08:16:14-04:00
17033|oO+iOLRrJCANgSCZeoETUs/6N+ycYU3Kw6QXUJAp89hBB1LzrYhnAzdZ1RSDV4ZauySapzTx87UVg2sjZdoJWw==|8.539|MelodicVixen|2021-10-03T11:42:32-04:00
42224|prDq4eY7ponR374ItzPtlvU7nKhfiPP1jpb/QVdzTjAnLx4vcJwPljmOT6Lp1xDtVZ+dBj74q3sv0EbapO8xOw==|6.314|AccessibleTinderbox|2021-02-27T17:15:47-05:00
35087|UfuHOq5VlgjmP3UDBH9/ZcJfylxpKi0g33YKiPsHCggjMfxUHiGT4iG4//6UQbYE3g8GnIK6dT2OLm2nqCSC6Q==|0.03|MelodicVixen|2021-12-23T20:12:42-05:00
12442|cRfvBpiYfCnXucHRFTHXVQSJkt/V4rZCVE0uGoOd5w5r8B1GNQ1ncyTzlRxKomeGDVL9IqBgVvSkhlkHLJwmJg==|4.434|TastelessHabitat|2021-09-23T04:27:31-04:00
37203|++fu9BV9+ffGVKHWqxdZgEna+YvDi6AAe3dpdg0/bDfnX/uU5juk9eisx4SS6n8tmV0rGCPzbjH8a4xeR1GJAg==|5.527|MelodicVixen|2021-02-02T09:41:27-05:00
48870|t/bd8NXCuu3rwU++fKZwaDiQRStigc7lriyrCxq9GVBkbIitA1nuh+MqJ58Pesdg0jCw2gTQNJPYHk3LwxsRkQ==|8.194|TriteBuddy|2021-01-19T20:43:27-05:00
28535|lrLnETOcFXWN5BsaZ3BqLLqjNo89Zw++vOWnBK7xwGg0Si4OcGYenbunMWLGEh0EDgOnUbrmL60mXanb61Z2XA==|8.781|DirefulKazoo|2021-06-14T23:51:02-04:00
35105|hkjon1IkZm90nljGiHBIDFp4PlfgovknPRLpKYcCnXV+j2XdGl+bkdQRzMhASJfhBu2XitW7EwjhZ4+4uJP0Hw==|2.92|DirefulKazoo|2021-11-28T02:49:04-05:00
17831|n2qX+Gb5LAvZTqpdbanrcLASVZECLzlpCou6tRx+il2maW3gk6Iahu1TkkaVw3vhP0BjYfnaqH1H0ZWNTal9VQ==|9.679|AbackColt|2021-07-12T18:44:13-04:00
44017|cAzn8EIv0ZUGYaWKVCIIEcPGw7f/T8zD5DdPn9ymRa87UhD1sGIs+R4iJYpO0/QYnEE/bOv/V9isx0ysm2eJzA==|6.879|AncientAncestor|2021-12-26T00:59:34-05:00
20345|VhCU6qiu+8p+VNBX0AO7ZfBU7OertGqFtEW4IVKC9KDIdKqn4QY+cGHF+G7kPJPXNhA3wGD8Xyn3AfP/PvZJhQ==|3.845|TriteBuddy|2021-12-31T13:38:16-05:00
48975|cyq5aqT2YOeviKsyPZtlygwHFLpEpdbMhRfMqFyG/WRrUfn51biVKri+MnCTl3XYhLXeThCxKhQpHWs6SRQlUg==|4.6|TastelessHabitat|2021-06-27T17:31:48-04:00
48077|ObIMVwUfyXd15VX9FODyjAtTg1J8u7t/RYl06SWmNLS0RoM9S1JoddaUSpEPlKhi+TPnY/8MtDLto3lUGr0zqw==|6.789|ElegantCreative|2021-07-29T08:13:15-04:00
36620|mvKrTOkM1Vn/UcxulCgRlPWWr3hsUg0irXWiuxfgtZevuNmLh49XJTFvb7Wf29e6xY+3mO3+s3mz7tE1Whd9iQ==|9.748|ElegantCreative|2021-12-20T18:44:50-05:00
46598|YCdO9dSQIUJJOZOBBjes/6vl2aGgNLKI4nzIghYZ7E09lgZvqCwFhzfHvNTYofewX2Ob6TpSiA5+66rv51DKvw==|9.363|TriteBuddy|2021-08-28T13:17:21-04:00
12685|6BRAGOQnjuHUHaKjHeUKCby1+trSUatoW49jyxUQySnaRdLj70+MwHRYxNvfjKE7vEFxwSLTdBK3ROEP50AZuw==|3.098|SulkyDryer|2021-01-06T14:04:28-05:00
20331|dCgam2c/fsYcmNZ+DXzQhgbfAF7UZo0Mu0d7cUNUB79dWOYuBxxOfX+d/gMqgGRAUMQTEnClceT+uD79FqkRxQ==|5.631|ElegantCreative|2021-09-06T05:46:53-04:00
19204|4O8o0Jk+JnjgPcpmfTj8QYvnVxwtVNBlvWHU0/QVYXUiLsPDULF+1uhGt9bGlqdZeHu2Cd32a0+RggFa78LONA==|3.708|SulkyDryer|2021-12-22T07:13:03-05:00
21062|YVOyM/Y0pyzpOfbStUaZPtJvA4hIhJ1C+ek2TzlSlu8oE80v+1e9eQtFUUyZC/eO81M30xwGn+DM39CBYYrRnw==|8.191|ThirstyChuck|2021-03-19T10:39:13-04:00
11463|DCc79X7cY/OPiuIyA3Xq7J0rfxQ5mQq3oBBxPJbK+RWH8RoO3ITkPkmJADg8xEXEtXUhBbkvB5dhBPrTbngwkQ==|8.462|ExpensivePoultry|2021-05-17T16:07:21-04:00
16358|WcoaHkX4CkB76TzpANQBviNySmpx3Uo/nFV/KKqnbL269hsqHKLSJAT0pF7goMlls/+7bScHE2VZfxjTaM8GIQ==|9.456|PlausibleEthyl|2021-10-20T16:11:19-04:00
43175|jSkeliwAPpId3xiWlvBluUf9wNH3FdVaSXSh9kb+Jpbvbm8My7EcSK63Xb9dLwgF0ZcO4G+7F2meC+I995r/fw==|2.524|AccessibleTinderbox|2021-11-21T03:09:16-05:00
29221|wRF68C2PaZqqM3Q1WZ5lorCE9AhlP5ot3Xqremplt+bISLyyvkUS2gYwA0wYAHeTdLeRYf6CJAW0VnP/HyVSEg==|4.175|PlausibleEthyl|2021-03-21T19:58:25-04:00
48488|BJ5BIUnIDv5K5OG8J8RM5bkPq1xPnsF2cdE58rFIAjrGJ1/D+3ElmiLxBkCMhLZP5e8Jonja6kVijxtjzXFUvQ==|8.611|DirefulKazoo|2021-06-30T15:15:29-04:00
35555|ZWw4kMDJx2RBoQBqvOs5FqwG5s1WLSjtRepkB2QStfdKZ9fSbXa9OrFDjaAudxKvJZ3g7Fbf7UITm9zO+qBiDA==|7.656|TastelessHabitat|2021-10-26T02:53:31-04:00
48456|+DWoj6SlOkh7qbsh2mF5SeCjVofIBAzYhbIw3WDmetiUNxsIai2P3O+0/gUkaHq/86S6eb+ScrwupbesQNgzUg==|3.863|ThirstyChuck|2021-06-01T15:53:18-04:00
46649|EcO+fPrcgQ7S7kwhX7HykJYgIo6TQvcr+SK521IcjfB7t6z2HR2rSpmR2LZB4jA4XwiMd9Ksltsmc67DgbISag==|5.974|AbackColt|2021-08-31T03:24:56-04:00
14139|qeNj6e2fe4B6Ymemz18VrGdVhH/dPibxE58CNpWOZbZoKW6PIGv0nEkqT04z2m5sg7y8LhSMI71/MZU8O8I9qA==|5.758|TriteBuddy|2021-01-14T23:58:05-05:00
45510|unbRIYv4y9iazvVmJEia/Y0QEXKDfsl8OfJlg1+UBjpHInIXtYWF4Mo8EhlgG5pMpB2jWOUG6tmaRtVQyfcZTg==|4.582|SulkyDryer|2021-06-11T22:50:36-04:00
48702|NzXwNnOzzR9IrX8gDQuNTAHpR9joPljt8LhnX05+xjsTmd4cAPqmec0tLymxNzKqKBHRBt0MPvtj04Zgwk6OEA==|0.051|AncientAncestor|2021-08-11T17:38:06-04:00
34962|jCDpd5UBYl/oulJwrA9+62AnvBdy3769U6XD1rDJEOq+hFZ0NBSRzatr7GEPUV7t5b4scwa+gHVM+Hjgx2n/8g==|1.104|TriteBuddy|2021-11-28T22:33:36-05:00
38737|dQ5dGrIISpqJtdLkvogGGaoHT8RIIprSjFLta3sLDNpG9P5SPTBtP7yfjsFgKEvImj0sdV5hMA9GQ4l9kl5sIg==|1.021|AbackColt|2021-07-09T03:57:16-04:00
42895|TKrDS/G3tLOi2tGyi9v7AZpjavpv2ZIZAfgjFc9bIyZ2FmI/MIOIAYUzFXA0ztbSD4xapZN/Jqmjc0aZEDv+IA==|3.25|DirefulKazoo|2021-08-14T10:34:05-04:00
37103|xg5Vtihq4SGtL7xugIZDC1t5yhTYUQ8yiYB2pOYFiGbCJHH7mzm9DyCIhvPIejLJivzHt0GQ+1AfqiQRUtHD/w==|8.643|MelodicVixen|2021-01-08T18:01:33-05:00
19231|oYKgQdIXcOQ64uhHtLRaSqSvWFUbpBem+WfXLh3qBfp7ctuV8dZSVdiOqaxTqKnBhnU/YAVpT0t5f6E6rOAGvA==|0.47|AncientAncestor|2021-07-29T02:56:42-04:00
44010|KEg0dkO/wvHamZw640X+VCutc412uK2Zw1zsACCGgEFuC1U7MPFneV0eK8JmLsqh9AkQJn2bTYzennMngsxOTg==|3.145|KaputStreet|2021-06-21T22:28:31-04:00
34270|Lg6yqR1Qt6WqmDMaziMR0WvgZMgTfstfQVlIf9ZcCxOkOX8yn1Bg0/FqzdL6tacJ784xvw+OiAt67htk9VjijA==|2.558|SulkyDryer|2021-06-02T08:11:19-04:00
35787|NlybVKjwmpMMCkBkeigZ5I51wtuvX68b9kJA31q9EDX3D8kwLns5+OlECUdYB/6XnxPZtZR/JTw4OBBXsGzBCw==|5.328|KaputStreet|2021-12-08T08:31:10-05:00
43007|dpMGeOUZRUSlPUCQYQAY//kgWa9ecO1pEqpXxaTBNBu+y2yzSRaN+NjhN5gpWiv4rrSDIarE8xV2mOpB4lB7Dg==|2.05|AbackColt|2021-05-08T12:13:53-04:00
28027|tuMyyq41yps4ndbvf+4Uk2aD35dMJgRHpzASGu+f8wBHszw8MEncbEWw351SQwMtfyZQ/WVofIUyOujVrGthnw==|2.089|PlausibleEthyl|2021-06-22T08:51:34-04:00
27885|klX5aPHNT6G1f+pSSZEmfEueWSTv+5aNc0ujr6QCAHzAKxNMfQM4uJdf31H64flgKbMty6s6p8qIwarwmwVTdg==|0.687|DirefulKazoo|2021-11-20T17:17:41-05:00
41456|A4gS6jQZKYfl3rzoV2XTH1AC3cpoufU+o1HHlUdfpFXz5vEHHpg+UKJ0kBByZ8sTR4kcI586CEzLy7yeBTxtbQ==|5.271|KaputStreet|2021-08-03T06:49:38-04:00
48797|FqjNh6W6z23gqxM+UUrDe8aC4/Cuq8zp/OWQZn+2IYY/l4oxvJLptzsRFtYROQlyy6tlON4aJIFhhj1xaGSa4Q==|4.168|ElegantCreative|2021-08-14T08:36:30-04:00
13432|BVzkqzINcXForIkAPD38X0/FaxccyNAphcefxlnkVDqI6WD3EHosQQuwozZdBylEpXEdk1r24MDQJ1BJTHxbUQ==|8.765|PlausibleEthyl|2021-01-20T23:02:05-05:00
30664|7+5ey//bkXMgjccFZhcdKEg5EfQF+ZOUa+++XauhNp7H2PARZqSJAww10D8y74IfA9c3KibFnXSKaQkFvqkifg==|5.492|ElegantCreative|2021-06-06T08:15:24-04:00
43519|2VPyosvv32Hru5LczTn9X4k2y5TOdFi8HkHI/ZKXOo1L2nrlfH9B/WjNnOVdTuUZJILgwj0QtbzU+atVfOTlPg==|1.79|AbackColt|2021-08-01T13:25:50-04:00
32610|y/u/VN0DhTXVxBy+q/inV/CsTgjkgxfmlDcPC7IGF+OHxE+goVTofO4+y61XsfZ8HsqTki0oOP+PirZXex5FpA==|3.901|AberrantReboot|2021-02-26T07:59:33-05:00
12499|hz4YoKaFCtbWITbMUPHJGSBEDzr/C1k+rTzPxWljkFBOV5KBe2me4lGlL02t26Bk3Hrr3WfOO3geeYcti+XUwQ==|8.036|PlausibleEthyl|2021-11-03T20:52:32-04:00
17618|mOlk7hJ8VmX0EgX0/w3ZOQoO5p/RQKD38hdKO5pxUzfoMTNweplj+02E1wGAwqTuZ+8wTMEcex9OYNjt40UPSQ==|3.334|AncientAncestor|2021-07-31T09:37:07-04:00
```

this is the only victim db row with a 5 digit customer ID:
```
13692|1.066|2022-06-17 14:29:39
```

Here is the corresponding key generation log entry:
```
2022-05-18T10:24:54-04:00	MelodicVixen	13692	1.066
```

MelodicVixen is the user we got creds for in task 6

Website landing page:
```
We regret to inform you that, due to recent system issues, we have been forced to rollback the key database to a backup from several months ago. We apologize for the inconvenience.
```

ransom page on task b1 has a demand of 1.066 as well
    https://jirwpbzkasgziwqr.unlockmyfiles.biz/

never got the tarball from task a2, it has a ransom.sh script that shows the uuid getting truncated to 128 bits, and then AES-128-CBC being used.

key: `449fc6e6-d6b6-11`

decrypt.py final decryption script, decrypt_all_ts.py recovers the key