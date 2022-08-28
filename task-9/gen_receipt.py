import jwt

with open("./debug/receipt.key", "r") as f:
    privkey = f.read()

body = {
    "customerID": "34962",
    "paymentAmount": 6.9,
}

payload = jwt.encode(body, key=privkey, algorithm="RS256")

print(payload)