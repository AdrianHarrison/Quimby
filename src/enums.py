from enum import IntEnum


class CryptoSrcEnum(IntEnum):
    CRYPTO = 0
    NACL = 1


class BitwiseOperationEnum(IntEnum):
    AND = 0
    OR = 1  #pylint: disable=invalid-name
    XOR = 2