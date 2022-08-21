import jwt
from datetime import datetime, timedelta

hmac_key = "ymQB3PsFosPGikNLLTiWwnYOpVdqXEBw"


sec = "aYGiCMKZc19HyuImYY7Bll5MWNwBe3bH"
uid = 2187

now = datetime.now()
exp = now + timedelta(days=30)
claims = {'iat': now,
          'exp': exp,
		  'uid': uid,
		  'sec': sec}
print(jwt.encode(claims, hmac_key, algorithm='HS256'))