import os
import unittest
import random

from src.hash import Hasher
from src.enums import CryptoSrcEnum

class TestEncryption(unittest.TestCase):

    def test_valid_scrypt_hash(self):
        for _ in range(10):
            salt = os.urandom(32)
            message = os.urandom(32)
            hasher = Hasher(CryptoSrcEnum.CRYPTO, salt)
            cryptoblock = hasher.hash(message)[:len(salt)]
            self.assertTrue(hasher.validate(message, cryptoblock))

    def test_invalid_scrypt_hash(self):
        for _ in range(10):
            salt = os.urandom(32)
            message = os.urandom(32)
            hasher = Hasher(CryptoSrcEnum.CRYPTO, salt)
            cryptoblock = hasher.hash(message)[:len(salt)]
            message = list(message)
            message[random.randrange(0, len(message))] = 11
            message = bytes(message)
            self.assertFalse(hasher.validate(message, cryptoblock))

    def test_invalid_scrypt_salt(self):
        for _ in range(10):
            salt = os.urandom(32)
            message = os.urandom(32)
            hasher = Hasher(CryptoSrcEnum.CRYPTO, salt)
            cryptoblock = hasher.hash(message)[:len(salt)]
            salt = os.urandom(32)
            hasher = Hasher(CryptoSrcEnum.CRYPTO, salt)
            self.assertFalse(hasher.validate(message, cryptoblock))


    def test_valid_nacl_hash(self):
        for _ in range(10):
            message = os.urandom(32)
            hasher = Hasher(CryptoSrcEnum.NACL)
            cryptoblock = hasher.hash(message)
            self.assertTrue(hasher.validate(message, cryptoblock))

    def test_invalid_nacl_hash(self):
        for _ in range(10):
            message = os.urandom(32)
            hasher = Hasher(CryptoSrcEnum.NACL)
            cryptoblock = hasher.hash(message)
            message = list(message)
            message[random.randrange(0, len(message))] = 11
            message = bytes(message)
            self.assertFalse(hasher.validate(message, cryptoblock))
