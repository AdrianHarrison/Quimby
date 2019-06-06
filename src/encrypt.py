"""
encrypt.py

Standard utility for encryption operations.
"""

from random import SystemRandom

from cryptography.fernet import Fernet  #pylint: disable=import-error
from nacl.secret import SecretBox  #pylint: disable=import-error
import nacl.utils as sodium_utils  #pylint: disable=import-error

from src.seed import Seeder
from src.enums import CryptoSrcEnum


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
            self._layer_key = Fernet.generate_key() if self.lib == CryptoSrcEnum.CRYPTO else sodium_utils.random(SecretBox.KEY_SIZE)

        return self._layer_key


    def encrypt(self, datablock: bytes) -> bytes:
        """ Performs encryption on the provided datablock
        with the seeded key.

        #TODO: LOOK AT TTL ON FERNET KEYS
        
        Arguments:
            datablock {bytes} -- Data to encrypt.
        
        Returns:
            bytes -- Encrypted block.
        """

        if self.lib == CryptoSrcEnum.CRYPTO:
            block = Fernet(self.layer_key).encrypt(datablock)
        else:
            block = SecretBox(self.layer_key).encrypt(datablock)

        return block
    
    def decrypt(self, datablock: bytes) -> bytes:
        """ Performs decryption on the provided datablock
        with the seeded key.
        
        Arguments:
            datablock {bytes} -- Data to decrypt.
        
        Returns:
            bytes -- Decrypted block.
        """

        if self.lib == CryptoSrcEnum.CRYPTO:
            block = Fernet(self.layer_key).decrypt(datablock)
        else:
            block = SecretBox(self.layer_key).decrypt(datablock)

        return block