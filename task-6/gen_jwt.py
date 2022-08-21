import jwt
from datetime import datetime, timedelta

hmac_key = "ymQB3PsFosPGikNLLTiWwnYOpVdqXEBw"


sec = "P5QQulqB5WeBuSoXNxPlBsqtDesIdjqC"
uid = 25761

now = datetime.now()
exp = now + timedelta(days=30)
claims = {'iat': now,
          'exp': exp,
		  'uid': uid,
		  'sec': sec}
print(jwt.encode(claims, hmac_key, algorithm='HS256'))