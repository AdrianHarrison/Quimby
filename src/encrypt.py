"""
encrypt.py

Standard utility for encryption operations.
"""

from src.seed import Seeder

from src.exceptions.key_exceptions import BadKeyException


class Encrypt():
    """ Main encryption tool, makes use of multifernet keys derived from
    generated user hashes.

    Attributes:
         _layer_key: The derived key specific to this layer. 
    """

    _layer_key = b""

    def __init__(self, layer_key: bytes):
            self._layer_key = None

    @property
    def _layer_key():
        if not self._layer_key:
            self._layer_key = Fernet(Seeder.seed_fernet_key())
            
        return self._layer_key 


    def encrypt(self, datablock: bytes) -> bytes:
        """ Primary encryption function, used to lock the next subsequent data 
        block.
        """
        fer = Fernet(self._layer_key)
        block = fer.encrypt(datablock)

        return block