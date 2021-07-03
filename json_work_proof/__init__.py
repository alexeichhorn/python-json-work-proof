from datetime import datetime, timedelta
from json_work_proof.base64url import *
from json_work_proof.json_encoder import DefaultJSONEncoder
from json_work_proof.classproperty import *
from typing import Optional
import hashlib
import logging
import json
import os

class JWP():

    def __init__(self, difficulty: int = 20, salt_length: int = 16):
        self.difficulty = difficulty
        self.salt_length = salt_length
    

    # - 

    class DateRange:
        def __init__(self, start: Optional[datetime], end: Optional[datetime]):
            self.start = start
            self.end = end
        
        @classmethod
        def start_until(cls, start: datetime, duration: timedelta):
            if isinstance(duration, float) or isinstance(duration, int): duration = timedelta(seconds=duration)
            return cls(start, start + duration)
        
        @classmethod
        def duration_to(cls, duration: timedelta, end: datetime):
            if isinstance(duration, float) or isinstance(duration, int): duration = timedelta(seconds=duration)
            return cls(end - duration, end)

        @classmethod
        def from_now(cls, duration: timedelta):
            return cls.start_until(datetime.now(), duration)
        
        @classproperty
        def unlimited(cls):
            return cls(None, None)
        
        # - Checks

        def contains(self, date: datetime):
            if self.start != None and date < self.start:
                return False
            elif self.end != None and date > self.end:
                return False
            else:
                return True
    

    # - Encode

    def generate(self, claims: dict, expiration: datetime = datetime.now() + timedelta(seconds=5*60)) -> str:

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

    def decode(self, stamp: str, verify: bool = True, expiration_range: DateRange = None) -> dict:
        '''
        :param expiration_range: defaults to a range from now to 30 minutes from now
        '''

        if expiration_range == None: expiration_range = JWP.DateRange.from_now(1800)

        components = stamp.split('.')
        if len(components) != 3: raise JWP.DecodeError.InvalidFormat

        encoded_header = components[0]
        encoded_body = components[1]

        header_data = base64url_decode(encoded_header)
        body_data = base64url_decode(encoded_body)

        header = json.loads(header_data)
        body = json.loads(body_data)

        if not verify: return body

        # TODO: check algorithm in header

        # - check proof

        hasher = hashlib.sha256()
        hasher.update(stamp.encode())
        digest = hasher.digest()

        if not self._is_zero_prefixed(digest, bit_count=self.difficulty):
            raise JWP.DecodeError.InvalidProof

        # - check expiration range

        expiration = body.get('exp', datetime.fromtimestamp(0))
        if isinstance(expiration, float) or isinstance(expiration, int): expiration = datetime.fromtimestamp(expiration)

        if not expiration_range.contains(expiration):
            raise JWP.DecodeError.Expired

        return body
    


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


    # - Exceptions

    class DecodeError:
        class InvalidFormat(Exception): pass
        class InvalidProof(Exception): pass
        class Expired(Exception): pass
