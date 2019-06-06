import os
import math
import unittest

from nacl.secret import SecretBox  #pylint: disable=import-error

from src.encrypt import Encrypt
from src.enums import CryptoSrcEnum

class TestEncryption(unittest.TestCase):

    def test_encrypt(self):
        """Tests to verify that the encryptor converts the input string
        into a different value.
        """
        for _ in range(100):
            encryptor = Encrypt()
            datastring = os.urandom(64)
            self.assertTrue(encryptor.encrypt(datastring) != datastring)

    def test_decrypt(self):
        """Tests to verify that the resulting string produced by encryptor
        can be used to decrypt the strings it creates.
        """
        for _ in range(100):
            encryptor = Encrypt()
            datastring = os.urandom(64)
            enc_string = encryptor.encrypt(datastring)
            self.assertTrue(encryptor.decrypt(enc_string) == datastring)
        

    def test_uniformity(self):
        for _ in range(100):
            encryptor = Encrypt()
            datastring = os.urandom(128)
            enc_string = encryptor.encrypt(datastring)
            

            if encryptor.lib == CryptoSrcEnum.CRYPTO:
                print("Not certain of expected fernet key length yet. Need to revisit.")
                # print(encryptor.lib)
                # print ((80 + ((math.ceil(len(datastring) / 16)+1) * 20)))
                # print(len(enc_string))
                # TODO: Revisit this, format for fernet bitsrting seems off, probably missing something
                # self.assertTrue(len(enc_string) == (80 + ((math.ceil(len(datastring) / 16)+1) * 20)))
            else:
                box = SecretBox(encryptor.layer_key)
                self.assertTrue(len(enc_string) == (len(datastring) + box.NONCE_SIZE + box.MACBYTES))
