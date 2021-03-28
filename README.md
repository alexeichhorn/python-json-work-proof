# JSON Work Proof

## Usage

### Generation

To generate a token, that proves you did work, create a `JWP`-object and call it with your dictionary of claims this:
```
from json_work_proof import JWP

jwp = JWP()
token = jwp.generate({ 'hello': 'world', 'count': 88 })
```

### Validation

To check if a token is valid for a certain difficulty and read the claims:
```
jwp = JWP()
try:
  claims = jwp.decode(token)
except JWP.DecodeError.InvalidFormat:
  print("The token is formatted incorrectly")
except JWP.DecodeError.InvalidProof:
  print("The difficulty this token was created at is lower than what is specified in your JWP object")
except JWP.DecodeError.Expired:
  print("The token expiration is too old or too new")
```

