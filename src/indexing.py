"""
indexing.py

Handles accessing, updating, and mutating byte strings.
"""

from src.enum import BitwiseOperationEnum


class Indexer():

    __OPERATION_MASK = {
        BitwiseOperationEnum.AND: (lambda src, mask: src & mask),
        BitwiseOperationEnum.OR: (lambda src, mask: src | mask),
        BitwiseOperationEnum.XOR: (lambda src, mask: src ^ mask),
    }

    @staticmethod
    def __safe_slice(byte_obj: bytes, l_idx: int, r_idx: int) -> bytes:
        """ Safely slices a bytes object returning the sliced segment.

        Arguments:
            byte_obj {bytes} -- Bytes to be sliced.
            l_idx {int} -- Leftmost index of the slice.
            r_idx {int} -- Rightmost index of the slice.

        Raises:
            IndexError: Raised if either bound is outside the bytes 
                object or the resulting slice is larger than intended. 

        Returns:
            bytes -- The sliced bytes object.
        """

        if l_idx < 0 or r_idx > len(byte_obj):
            raise IndexError

        sliced = byte_obj[l_idx:r_idx]

        if len(sliced) != (r_idx - l_idx):
            raise IndexError

        return sliced

    @classmethod
    def left_slice(cls, byte_obj: bytes, idx: int,
                   destroy: bool = True) -> tuple:
        """ Slices bytes off of the leftmost side of a bytes object.

        Arguments:
            byte_obj {bytes} -- Bytes to be sliced.
            idx {int} -- Rightmost index of the slice.

        Keyword Arguments:
            destroy {bool} -- Whether or not to remove the sliced range
                from the source bytes (default: {True})

        Returns:
            tuple -- Resulting bytes object and sliced segment.
        """

        sliced = cls.__safe_slice(byte_obj, 0, idx)
        base = cls.__safe_slice(byte_obj, idx,
                                len(byte_obj)) if destroy else byte_obj
        return (base, sliced)

    @classmethod
    def right_slice(cls, byte_obj: bytes, idx: int,
                    destroy: bool = True) -> tuple:
        """ Slices bytes off of the rightmost side of a bytes object.

        Arguments:
            byte_obj {bytes} -- Bytes to be sliced.
            idx {int} -- Leftmost index of the slice.

        Keyword Arguments:
            destroy {bool} -- Whether or not to remove the sliced range
                from the source bytes (default: {True})

        Returns:
            tuple -- Resulting bytes object and sliced segment.
        """

        sliced = cls.__safe_slice(byte_obj, len(byte_obj - idx), len(byte_obj))
        base = cls.__safe_slice(byte_obj, 0, len(byte_obj -
                                                 idx)) if destroy else byte_obj
        return (base, sliced)

    @classmethod
    def bisect_index(cls,
                     byte_obj: bytes,
                     l_idx: int,
                     r_idx: int,
                     l_destroy: bool = True,
                     r_destroy: bool = True) -> tuple:
        """ Slices bytes off of the both sides of a bytes object.

        Arguments:
            byte_obj {bytes} -- Bytes to be sliced.
            l_idx {int} -- Rightmost index of the left slice.
            r_idx {int} -- Leftmost index of the right slice.

        Keyword Arguments:
            l_destroy {bool} -- Whether or not to remove the leftmost
                sliced range from the source bytes (default: {True})
            r_destroy {bool} -- Whether or not to remove the rightmost
                sliced range from the source bytes (default: {True}

        Returns:
            tuple -- Resulting bytes object and the left and right
                sliced segments.
        """

        return (byte_obj, cls.left_slice(byte_obj, l_idx, l_destroy),
                cls.right_slice(byte_obj, r_idx, r_destroy))

    @classmethod
    def mask(cls,
             source: bytes,
             mask: bytes,
             operation: BitwiseOperationEnum = BitwiseOperationEnum.AND
            ) -> bytes:
        """ Pulls a mask out of a bytestring. Used for deriving multiple
        keys from an individual string.

        Arguments:
            source {bytes} -- Bytes to be masked.
            mask {bytes} -- Mask to apply to bytes.

        Keyword Arguments:
            operation {bool} -- Bitwise operation to perform.
                (default: {BitwiseOperationEnum.AND})

        Raises:
            IndexError: Raised if the source and mask have differing
                lengths

        Returns:
            bytes -- Masked bytes object.
        """

        if len(source) != len(mask):
            raise IndexError

        output = b""

        for idx, _ in enumerate(source):
            output += chr(cls.__OPERATION_MASK[operation](source[idx],
                                                          mask[idx])).encode()

        return output
