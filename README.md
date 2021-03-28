# JSON Work Proof

## Usage

### General

To generate and validate tokens you need to use a `JWP`-object. On creation you can specify the `difficulty`, which determines how hard the challenge should be. It defaults to `20`, which takes about a second to compute on an average computer. Each increment by one, doubles the difficulty and therefore the time it takes to generate.
```
from json_work_proof import JWP

jwp = JWP() # defaults to difficulty=20
jwp_harder = JWP(difficulty=25)
```

### Generation

To generate a token, that proves you did work, create a `JWP`-object and call it with your dictionary of claims like this:
```
jwp = JWP()
token = jwp.generate({ 'hello': 'world', 'count': 88 })
```

*Note:* A token expires 5 minutes after creation on default. You can change this by giving a custom expiration date:
```
expiration = datetime.utcnow() + timedelta(hours=1) # 1 hour from now
token = jwp.generate(claims, expiration=expiration)
```


### Validation

To check if a token is valid for a certain difficulty and to read the claims:
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

