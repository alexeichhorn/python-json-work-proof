import unittest
import random
import time
from json_work_proof import JWP

class JWPTests(unittest.TestCase):
    
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

            self.assertEqual(claims['hello'], decodedClaims['hello'])
            self.assertEqual(claims['randomInt'], decodedClaims['randomInt'])
    

    def dtest_generate_and_check(self):
        self.generate_and_check(JWP(), count=5)
        self.generate_and_check(JWP(difficulty=22), count=2)
        self.generate_and_check(JWP(difficulty=18), count=5)
        self.generate_and_check(JWP(difficulty=15), count=10)
        self.generate_and_check(JWP(difficulty=5), count=10)
        self.generate_and_check(JWP(difficulty=15, salt_length=100), count=5)
    

    def dtest_zero_bit_count(self):
        jwp = JWP()
        self.assertEqual(jwp._leading_zero_bit_count(0b1000_0000), 0)
        self.assertEqual(jwp._leading_zero_bit_count(0b0100_0000), 1)
        self.assertEqual(jwp._leading_zero_bit_count(0b0010_0000), 2)
        self.assertEqual(jwp._leading_zero_bit_count(0b0001_0000), 3)
        self.assertEqual(jwp._leading_zero_bit_count(0b0000_1000), 4)
        self.assertEqual(jwp._leading_zero_bit_count(0b0000_0100), 5)
        self.assertEqual(jwp._leading_zero_bit_count(0b0000_0010), 6)
        self.assertEqual(jwp._leading_zero_bit_count(0b0000_0001), 7)
        self.assertEqual(jwp._leading_zero_bit_count(0), 8)


if __name__ == '__main__':
    unittest.main()