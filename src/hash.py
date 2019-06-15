"""
hash.py

Standard utility for hashing operations.
"""

import os
from random import SystemRandom

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt #pylint: disable=import-error
from cryptography.hazmat.backends import default_backend #pylint: disable=import-error
from cryptography.exceptions import InvalidKey #pylint: disable=import-error
from nacl.pwhash import argon2id  #pylint: disable=import-error
from nacl.exceptions import InvalidkeyError #pylint: disable=import-error

from src.enums import CryptoSrcEnum


class Hasher():
    """ Main encryption tool, makes use of multifernet keys derived from
    generated user hashes.

    Attributes:
        lib: The specific library to use to perform one way hashing.
        salt: Salt to be used with Scrypt keys
        _SCRYPT_LEN: Length parameter used in scrypt hashing.
        _SCRYPT_MEM: Memory requirement parameter used in scrypt hashing.
        _SCRYPT_BLOCK: Block size parameter used in scrypt hashing.
        _SCRYPT_PARALELL: Parallelization parameter used in scrypt hashing.
    """

    lib = None
    salt = None

    _SCRYPT_LEN = 32
    _SCRYPT_MEM = 1048576 # 2**20
    _SCRYPT_BLOCK = 8
    _SCRYPT_PARALELL = 1

    def __init__(self, lib: CryptoSrcEnum, salt: bytes = None):
        self.lib = SystemRandom().choice(
            [CryptoSrcEnum.CRYPTO, CryptoSrcEnum.NACL]) if lib not in (CryptoSrcEnum.CRYPTO, CryptoSrcEnum.NACL) else lib
        self.salt = salt

    def __srcypt_obj(self) -> Scrypt:
        """ Helper method to encapsulate the creation of scrypt objects.

        Returns:
            Scrypt -- Scrypt object for use by the application.
        """

        return Scrypt(
            salt=self.salt,
            length=self._SCRYPT_LEN,
            n=self._SCRYPT_MEM,
            r=self._SCRYPT_BLOCK,
            p=self._SCRYPT_PARALELL,
            backend=default_backend()
        )


    def __crypto_hash(self, message: bytes) -> bytes:
        """ Performs a one way hash using cryptography / Scrypt.

        Keyword Arguments:
            message {bytes} -- Bytestring message to be encrypted.

        Returns:
            bytes -- Scrypt hash combined with salt.
        """

        return self.__srcypt_obj().derive(message) + self.salt

    def __nacl_hash(self, message: bytes) -> bytes:
        """Performs a one way hash using NaCl / Argon2id.

        Arguments:
            message {bytes} -- Bytestring message to be encrypted.

        Returns:
            bytes -- NaCl hash bytestring.
        """

        return argon2id.str(message)

    def __crypto_validate(self, message: bytes, key: bytes) -> bool:
        """ Validates a Scrypt hash against a provided password.

        Arguments:
            message {bytes} -- User input to validate.
            key {bytes} -- Scrypt hash bytestring.

        Returns:
            bool -- Result of the validation attempt.
        """

        try:
            self.__srcypt_obj().verify(message, key)
            return True
        except InvalidKey:
            return False

    def __nacl_validate(self, message: bytes, key: bytes) -> bool:
        """ Validates a NaCl hash against a provided password.

        Arguments:
            message {bytes} -- User input to validate.
            key {bytes} -- NaCl hash bytestring.

        Returns:
            bool -- Result of the validation attempt.
        """

        try:
            return argon2id.verify(key, message)
        except InvalidkeyError:
            return False

    def hash(self, message: bytes) -> bytes:
        """ Wrapper function for simplified hashing.

        Arguments:
            message {bytes} -- Bytestring to be hashed.

        Returns:
            bytes -- The resulting hash bytestring.
        """

        return self.__crypto_hash(message) if self.lib == CryptoSrcEnum.CRYPTO else self.__nacl_hash(message)

    def validate(self, message: bytes, key: bytes) -> bool:
        """ Wrapper function for simplified validation.

        Arguments:
            message {bytes} -- Bytestring to be hashed.
            key {bytes} -- Key value to validate against.

        Returns:
            bool -- Result of the validation attempt.
        """

        return self.__crypto_validate(message, key) if self.lib == CryptoSrcEnum.CRYPTO else self.__nacl_validate(message, key)
