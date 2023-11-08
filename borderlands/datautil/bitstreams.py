import copy


class ReadBitstream:
    def __init__(self, s: bytes) -> None:
        self.s = s
        self.i = 0

    def read_bit(self) -> int:
        i = self.i
        self.i = i + 1
        byte = self.s[i >> 3]
        bit = byte >> (7 - (i & 7))
        return bit & 1

    def read_bits(self, n: int) -> int:
        s = self.s
        i = self.i
        end = i + n
        chunk = s[i >> 3 : (end + 7) >> 3]
        value = chunk[0] & ~(0xFF00 >> (i & 7))
        for c in chunk[1:]:
            value = (value << 8) | c
        if (end & 7) != 0:
            value = value >> (8 - (end & 7))
        self.i = end
        return value

    def read_byte(self) -> int:
        i = self.i
        self.i = i + 8
        byte = self.s[i >> 3]
        if (i & 7) == 0:
            return byte
        byte = (byte << 8) | self.s[(i >> 3) + 1]
        return (byte >> (8 - (i & 7))) & 0xFF


class WriteBitstream:
    def __init__(self) -> None:
        self.s = bytearray()
        self.byte = 0
        self.i = 7

    def write_bit(self, b: int) -> None:
        i = self.i
        byte = self.byte | (b << i)
        if i == 0:
            self.s.append(byte)
            self.byte = 0
            self.i = 7
        else:
            self.byte = byte
            self.i = i - 1

    def write_bits(self, b: int, n: int) -> None:
        s = self.s
        byte = self.byte
        i = self.i
        while n >= (i + 1):
            shift = n - (i + 1)
            n = n - (i + 1)
            byte = byte | (b >> shift)
            b = b & ~(byte << shift)
            s.append(byte)
            byte = 0
            i = 7
        if n > 0:
            byte = byte | (b << (i + 1 - n))
            i = i - n
        self.s = s
        self.byte = byte
        self.i = i

    def write_byte(self, b: int) -> None:
        i = self.i
        if i == 7:
            self.s.append(b)
        else:
            self.s.append(self.byte | (b >> (7 - i)))
            self.byte = (b << (i + 1)) & 0xFF

    def getvalue(self) -> bytes:
        if self.i != 7:
            ret_s = copy.copy(self.s)
            ret_s.append(self.byte)
            return bytes(ret_s)
        else:
            return bytes(self.s)
