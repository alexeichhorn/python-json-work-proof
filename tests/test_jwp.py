import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
import random
import time
from datetime import datetime
from json_work_proof import JWP

class TestJWP:
    
    def test_single(self):
        start = time.time()
        jwp = JWP(difficulty=20)
        token = jwp.generate({ 'hello': 'world' })
        print(token)
        print("took %.3f s" % (time.time() - start))


    def generate_and_check(self, jwp: JWP, count: int = 10):
        for _ in range(count):
            claims = { 'hello': 'world', 'randomInt': random.randint(0, 1000000000) }
            stamp = jwp.generate(claims)

            decodedClaims = jwp.decode(stamp)

            assert claims['hello'] == decodedClaims['hello']
            assert claims['randomInt'] == decodedClaims['randomInt']
    

    def test_generate_and_check(self):
        self.generate_and_check(JWP(), count=5)
        self.generate_and_check(JWP(difficulty=22), count=2)
        self.generate_and_check(JWP(difficulty=18), count=5)
        self.generate_and_check(JWP(difficulty=15), count=10)
        self.generate_and_check(JWP(difficulty=5), count=10)
        self.generate_and_check(JWP(difficulty=15, salt_length=100), count=5)


    def test_expiration_check(self):
        jwp = JWP(difficulty=20)

        stamp1 = "eyJ0eXAiOiJKV1AiLCJhbGciOiJTSEEyNTYiLCJkaWYiOjIwfQ.eyJleHAiOjE2MTY4NTA1NzAuNjU1MTQ3MSwiaGVsbG8iOiJ3b3JsZCJ9.VE6YYxIQ46lPzxyNuRYAmAMkEM"
        assert isinstance(jwp.decode(stamp1, expiration_range=JWP.DateRange.unlimited), dict)
        assert isinstance(jwp.decode(stamp1, expiration_range=JWP.DateRange.start_until(datetime.fromtimestamp(1616850383), 5*60)), dict)
        with pytest.raises(JWP.DecodeError.Expired):
            jwp.decode(stamp1)
        
        stamp2 = "eyJ0eXAiOiJKV1AiLCJhbGciOiJTSEEyNTYiLCJkaWYiOjIwfQ.eyJoZWxsbyI6IndvcmxkIn0.LCYdFqTlHkox8chJLRoPpQB5wC"
        assert isinstance(jwp.decode(stamp2, expiration_range=JWP.DateRange.unlimited))
        with pytest.raises(JWP.DecodeError.Expired):
            jwp.decode(stamp2)
        with pytest.raises(JWP.DecodeError.Expired):
            jwp.decode(stamp2, expiration_range=JWP.DateRange.duration_to(1_000_000, datetime.now()))
        assert isinstance(jwp.decode(stamp2, expiration_range=JWP.DateRange(None, datetime.now())))
    

    def test_difficulty_check(self):
        hard_jwp = JWP(difficulty=20)
        easy_jwp = JWP(difficulty=15)

        hard_stamp = "eyJ0eXAiOiJKV1AiLCJhbGciOiJTSEEyNTYiLCJkaWYiOjIwfQ.eyJleHAiOjE2MTY4NTA1NzAuNjU1MTQ3MSwiaGVsbG8iOiJ3b3JsZCJ9.VE6YYxIQ46lPzxyNuRYAmAMkEM"
        easy_stamp = "eyJ0eXAiOiJKV1AiLCJhbGciOiJTSEEyNTYiLCJkaWYiOjE1fQ.eyJoZWxsbyI6IndvcmxkIiwiZXhwIjoxNjE2ODUxODcyLjUyOTQwNDJ9.Rg1tRi9JUkw1Ls9WotkuaAFzs"

        assert isinstance(hard_jwp.decode(hard_stamp, expiration_range=JWP.DateRange.unlimited), dict)
        with pytest.raises(JWP.DecodeError.InvalidProof):
            hard_jwp.decode(easy_stamp, expiration_range=JWP.DateRange.unlimited)
        
        assert isinstance(easy_jwp.decode(hard_stamp, expiration_range=JWP.DateRange.unlimited), dict)
        assert isinstance(easy_jwp.decode(easy_stamp, expiration_range=JWP.DateRange.unlimited), dict)
    

    def test_invalid_proof_check(self):
        jwp = JWP(difficulty=20)

        valid_stamp = "eyJ0eXAiOiJKV1AiLCJhbGciOiJTSEEyNTYiLCJkaWYiOjIwfQ.eyJleHAiOjE2MTY4NTA1NzAuNjU1MTQ3MSwiaGVsbG8iOiJ3b3JsZCJ9.VE6YYxIQ46lPzxyNuRYAmAMkEM"
        assert isinstance(jwp.decode(valid_stamp, expiration_range=JWP.DateRange.unlimited))

        invalid_stamp = "eyJ0eXAiOiJKV1AiLCJhbGciOiJTSEEyNTYiLCJkaWYiOjIwfQ.eyJleHAiOjE2MTY4NTA1NzAuNjU1MTQ3MSwiaGVsbG8iOiJ3b3JsZCJ9.VE6YYxIQ46lPzxyNuRYAmAMkEC"
        assert isinstance(jwp.decode(invalid_stamp, verify=False), dict)
        with pytest.raises(JWP.DecodeError.InvalidProof):
            jwp.decode(invalid_stamp, expiration_range=JWP.DateRange.unlimited)
    


    def test_zero_bit_count(self):
        jwp = JWP()
        assert jwp._leading_zero_bit_count(0b1000_0000) == 0
        assert jwp._leading_zero_bit_count(0b0100_0000) == 1
        assert jwp._leading_zero_bit_count(0b0010_0000) == 2
        assert jwp._leading_zero_bit_count(0b0001_0000) == 3
        assert jwp._leading_zero_bit_count(0b0000_1000) == 4
        assert jwp._leading_zero_bit_count(0b0000_0100) == 5
        assert jwp._leading_zero_bit_count(0b0000_0010) == 6
        assert jwp._leading_zero_bit_count(0b0000_0001) == 7
        assert jwp._leading_zero_bit_count(0) == 8
