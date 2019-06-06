import os
import unittest

from src.indexing import Indexer

class TestEncryption(unittest.TestCase):

    def test_left_slice_destructive(self):
        """ Tests a destructive left slice."""
        datastring = b"000000111111"
        left, right = Indexer.left_slice(datastring, 6)
        self.assertTrue(left == b"000000")
        self.assertTrue(right == b"111111")

    def test_left_slice_safe(self):
        """ Tests a safe left slice."""
        datastring = b"000000111111"
        left, safe = Indexer.left_slice(datastring, 6, destroy=False)
        self.assertTrue(left == b"000000")
        self.assertTrue(safe == datastring)

