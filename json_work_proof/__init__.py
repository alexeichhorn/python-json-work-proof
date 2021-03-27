from datetime import datetime, timedelta
from json_work_proof.base64url import *
from json_work_proof.json_encoder import DefaultJSONEncoder
import hashlib
import logging
import json
import os

class JWP():

    def __init__(self, difficulty: int = 20, salt_length: int = 16):
        self.difficulty = difficulty
        self.salt_length = salt_length
    

    # - Encode

    def generate(self, claims: dict, expiration: datetime = datetime.utcnow() + timedelta(seconds=5*60)) -> str:

        header = { 'typ': 'JWP', 'alg': 'SHA256', 'dif':  self.difficulty }

        if expiration != None and 'exp' not in claims:
            claims['exp'] = expiration
        
        body = DefaultJSONEncoder().encode(claims)
        encodedBody = base64url_encode(body)
        encodedHeader = base64url_encode(DefaultJSONEncoder().encode(header))

        salt = self._generate_salt()
        encodedSalt = base64url_encode(salt)

        challenge = encodedHeader + b"." + encodedBody + b"." + encodedSalt

        counter = 0
        representing_bytes = 0

        while True:
            proof = None
            while proof == None:
                try:
                    proof = counter.to_bytes(representing_bytes, 'big')
                except OverflowError:
                    representing_bytes += 1
            
            encodedProof = base64url_encode(proof)

            hasher = hashlib.sha256()
            hasher.update(challenge)
            hasher.update(encodedProof)
            digest = hasher.digest()

            if self._is_zero_prefixed(digest, bit_count=self.difficulty):
                return challenge.decode('utf-8') + encodedProof.decode('utf-8')
            
            counter += 1


    # - Decode

    def decode(self, stamp: str, verify: bool = True) -> dict:
        return {}
    


    # - Helpers

    def _is_zero_prefixed(self, data, bit_count: int) -> bool:
        for byte in data:
            if bit_count == 0: return True

            if bit_count >= 8:
                if byte != 0: return False
                bit_count -= 8
            else:
                return self._leading_zero_bit_count(byte) >= bit_count
    
    def _leading_zero_bit_count(self, byte) -> int:
        mask = 0b1000_0000
        for i in range(8):
            masked_bit = byte & mask
            mask >>= 1
            if masked_bit != 0:
                return i
        return 8


    def _generate_salt(self):
        return os.urandom(self.salt_length)