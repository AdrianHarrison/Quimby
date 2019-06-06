import os
import unittest

from src.indexing import Indexer

class TestEncryption(unittest.TestCase):
    
    _BASE = b"000000111111"
    _LEFT = b"000000"
    _LEFT_SHORT = b"000"
    _RIGHT = b"111111"
    _RIGHT_SHORT = b"111"
    _CENTER = b"000111"
    _MASK = b"101010101010"

    def test_left_slice_destructive(self):
        """ Tests a destructive left slice."""
        left, right = Indexer.left_slice(self._BASE, 6)
        self.assertTrue(left == self._LEFT)
        self.assertTrue(right == self._RIGHT)

    def test_left_slice_safe(self):
        """ Tests a safe left slice."""
        left, safe = Indexer.left_slice(self._BASE, 6, destroy=False)
        self.assertTrue(left == self._LEFT)
        self.assertTrue(safe == self._BASE)

    def test_right_slice_destructive(self):
        """ Tests a destructive right slice."""
        right, left = Indexer.right_slice(self._BASE, 6)
        self.assertTrue(right == self._RIGHT)
        self.assertTrue(left == self._LEFT)

    def test_right_slice_safe(self):
        """ Tests a safe right slice."""
        right, safe = Indexer.right_slice(self._BASE, 6, destroy=False)
        self.assertTrue(right == self._RIGHT)
        self.assertTrue(safe == self._BASE)

    def test_bisect_destructive(self):
        """ Tests a destructive bisect."""
        left, right, center = Indexer.bisect_index(self._BASE, 3, 3)
        self.assertTrue(left == self._LEFT_SHORT)
        self.assertTrue(right == self._RIGHT_SHORT)
        self.assertTrue(center == self._CENTER)

    def test_bisect_safe(self):
        """ Tests a safe bisect."""
        left, right, center = Indexer.bisect_index(self._BASE, 3, 3, l_destroy=False, r_destroy=False)
        self.assertTrue(left == self._LEFT_SHORT)
        self.assertTrue(right == self._RIGHT_SHORT)
        self.assertTrue(center == self._BASE)

