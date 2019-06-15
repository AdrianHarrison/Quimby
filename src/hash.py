"""
hash.py

Standard utility for hashing operations.
"""

import os
from random import SystemRandom

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt #pylint: disable=import-error
from cryptography.hazmat.backends import default_backend #pylint: disable=import-error
from nacl.pwhash import argon2id  #pylint: disable=import-error
from nacl.exceptions import InvalidkeyError #pylint: disable=import-error

from src.enums import CryptoSrcEnum


class Hasher():
    """ Main encryption tool, makes use of multifernet keys derived from
    generated user hashes.

    Attributes:
         lib: The specific library to use to perform one way hashing. 
    """

    lib = None

    _SCRYPT_LEN = 32
    _SCRYPT_MEM = 1048576 # 2**20
    _SCRYPT_BLOCK = 8
    _SCRYPT_PARALELL = 1



    def __init__(self, lib: CryptoSrcEnum):
        self.lib = SystemRandom().choice(
            [CryptoSrcEnum.CRYPTO, CryptoSrcEnum.NACL]) if not lib else lib


    @classmethod
    def __crypto_hash(cls, message=bytes, salt=bytes) -> bytes:
        """[summary]
        
        Keyword Arguments:
            message {[type]} -- [description] (default: {bytes})
            salt {[type]} -- [description] (default: {bytes})
        """
        return Scrypt(
            salt=salt,
            length=cls._SCRYPT_LEN,
            n=cls._SCRYPT_MEM,
            r=cls._SCRYPT_BLOCK,
            p=cls._SCRYPT_PARALELL,
            backend=default_backend
        ).derive(message) + salt

    @classmethod
    def __nacl_hash(cls, message=bytes) -> tuple:
        """[summary]
        
        Keyword Arguments:
            message {[type]} -- [description] (default: {bytes})
            salt {[type]} -- [description] (default: {bytes})
        
        Returns:
            tuple -- [description]
        """
        return (argon2id.str(message),)

    @classmethod
    def __crypto_validate(cls, message=bytes, key=bytes, salt=bytes) -> bool:
        """[summary]
        
        Keyword Arguments:
            message {[type]} -- [description] (default: {bytes})
            salt {[type]} -- [description] (default: {bytes})
        """
        return Scrypt(
            salt=salt,
            length=cls._SCRYPT_LEN,
            n=cls._SCRYPT_MEM,
            r=cls._SCRYPT_BLOCK,
            p=cls._SCRYPT_PARALELL,
            backend=default_backend
        ).verify(message, key)

    @classmethod
    def __nacl_validate(cls, message: bytes, key: bytes) -> bool:
        """[summary]
        
        Keyword Arguments:
            message {[type]} -- [description] (default: {bytes})
            salt {[type]} -- [description] (default: {bytes})
        
        Returns:
            tuple -- [description]
        """
        try:
            argon2id.verify(message, key)
            return True
        except InvalidkeyError:
            return False

    def hash(self, message=bytes, salt_seed=int) -> bytes:
        """[summary]
        
        Keyword Arguments:
            message {[type]} -- [description] (default: {bytes})
            salt {[type]} -- [description] (default: {bytes})
        """

        return self.__crypto_hash(message, os.urandom(salt_seed)) if self.lib == CryptoSrcEnum.CRYPTO else self.__nacl_hash(message)
    
    def validate(self, message: bytes, key: bytes, salt: bytes = None) -> bool:
        """[summary]
        
        Arguments:
            message {bytes} -- [description]
            key {bytes} -- [description]
        
        Keyword Arguments:
            salt {bytes} -- [description] (default: {None})
        """

        return self.__crypto_validate(message, key, salt) if self.lib == CryptoSrcEnum.CRYPTO else self.__nacl_validate(message, key)
