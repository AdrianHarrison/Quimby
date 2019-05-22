"""
encrypt.py

Standard utility for encryption operations.
"""

from random import SystemRandom

from cryptography import Fernet  #pylint: disable=import-error
from nacl.secret import SecretBox  #pylint: disable=import-error
import nacl.utils as sodium_utils  #pylint: disable=import-error

from src.seed import Seeder
from src.enum import CryptoSrcEnum


class Encrypt():
    """ Main encryption tool, makes use of multifernet keys derived from
    generated user hashes.

    Attributes:
         _layer_key: The derived key specific to this layer. 
    """

    _layer_key = b""
    lib = None

    def __init__(self):
        self.lib = SystemRandom().choice(
            [CryptoSrcEnum.CRYPTO, CryptoSrcEnum.NACL])
        self._layer_key = None

    @property
    def layer_key(self):
        if not self._layer_key:
            self._layer_key = Fernet(Seeder.seed_encryption_key())

        return self._layer_key

    def encrypt_fernet(self, datablock: bytes) -> bytes:
        """ Performs fernet encryption on the provided datablock
        with the seeded key.
        
        Arguments:
            datablock {bytes} -- Data to encrypt.
        
        Returns:
            bytes -- Encrypted block.
        """

        fer = Fernet(self._layer_key)
        block = fer.encrypt(datablock)

        return block