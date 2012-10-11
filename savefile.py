#! /usr/bin/env python

from bisect import insort
from cStringIO import StringIO
import hashlib
import json
import optparse
import struct
import sys

import lzo


class BL2Error(Exception): pass


class ReadBitstream(object):

    def __init__(self, s):
        self.s = s
        self.i = 0

    def read_bit(self):
        i = self.i
        self.i = i + 1
        byte = ord(self.s[i >> 3])
        bit = byte >> (7 - (i & 7))
        return bit & 1

    def read_bits(self, n):
        s = self.s
        i = self.i
        end = i + n
        chunk = s[i >> 3: (end + 7) >> 3]
        value = ord(chunk[0]) &~ (0xff00 >> (i & 7))
        for c in chunk[1: ]:
            value = (value << 8) | ord(c)
        if (end & 7) != 0:
            value = value >> (8 - (end & 7))
        self.i = end
        return value

    def read_byte(self):
        i = self.i
        self.i = i + 8
        byte = ord(self.s[i >> 3])
        if (i & 7) == 0:
            return byte
        byte = (byte << 8) | ord(self.s[(i >> 3) + 1])
        return (byte >> (8 - (i & 7))) & 0xff

class WriteBitstream(object):

    def __init__(self):
        self.s = ""
        self.byte = 0
        self.i = 7

    def write_bit(self, b):
        i = self.i
        byte = self.byte | (b << i)
        if i == 0:
            self.s += chr(byte)
            self.byte = 0
            self.i = 7
        else:
            self.byte = byte
            self.i = i - 1

    def write_bits(self, b, n):
        s = self.s
        byte = self.byte
        i = self.i
        while n >= (i + 1):
            shift = n - (i + 1)
            n = n - (i + 1)
            byte = byte | (b >> shift)
            b = b &~ (byte << shift)
            s = s + chr(byte)
            byte = 0
            i = 7
        if n > 0:
            byte = byte | (b << (i + 1 - n))
            i = i - n
        self.s = s
        self.byte = byte
        self.i = i

    def write_byte(self, b):
        i = self.i
        if i == 7:
            self.s += chr(b)
        else:
            self.s += chr(self.byte | (b >> (7 - i)))
            self.byte = (b << (i + 1)) & 0xff

    def getvalue(self):
        if self.i != 7:
            return self.s + chr(self.byte)
        else:
            return self.s


def read_huffman_tree(b):
    node_type = b.read_bit()
    if node_type == 0:
        return (None, (read_huffman_tree(b), read_huffman_tree(b)))
    else:
        return (None, b.read_byte())

def write_huffman_tree(node, b):
    if type(node[1]) is int:
        b.write_bit(1)
        b.write_byte(node[1])
    else:
        b.write_bit(0)
        write_huffman_tree(node[1][0], b)
        write_huffman_tree(node[1][1], b)

def make_huffman_tree(data):
    frequencies = [0] * 256
    for c in data:
        frequencies[ord(c)] += 1

    nodes = [[f, i] for (i, f) in enumerate(frequencies) if f != 0]
    nodes.sort()

    while len(nodes) > 1:
        l, r = nodes[: 2]
        nodes = nodes[2: ]
        insort(nodes, [l[0] + r[0], [l, r]])

    return nodes[0]

def invert_tree(node, code=0, bits=0):
    if type(node[1]) is int:
        return {chr(node[1]): (code, bits)}
    else:
        d = {}
        d.update(invert_tree(node[1][0], code << 1, bits + 1))
        d.update(invert_tree(node[1][1], (code << 1) | 1, bits + 1))
        return d

def huffman_decompress(tree, bitstream, size):
    output = ""
    while len(output) < size:
        node = tree
        while 1:
            b = bitstream.read_bit()
            node = node[1][b]
            if type(node[1]) is int:
                output += chr(node[1])
                break
    return output

def huffman_compress(encoding, data, bitstream):
    for c in data:
        code, nbits = encoding[c]
        bitstream.write_bits(code, nbits)


item_sizes = (
    (8, 17, 20, 11, 7, 7, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16),
    (8, 13, 20, 11, 7, 7, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17)
)

def pack_item_values(is_weapon, values):
    i = 0
    bytes = [0] * 32
    for value, size in zip(values, item_sizes[is_weapon]):
        if value is None:
            break
        j = i >> 3
        value = value << (i & 7)
        while value != 0:
            bytes[j] |= value & 0xff
            value = value >> 8
            j = j + 1
        i = i + size
    return "".join(map(chr, bytes[: (i + 7) >> 3]))

def unpack_item_values(is_weapon, data):
    i = 8
    data = " " + data
    values = []
    end = len(data) * 8
    for size in item_sizes[is_weapon]:
        j = i + size
        if j > end:
            values.append(None)
            continue
        value = 0
        for b in data[j >> 3: (i >> 3) - 1: -1]:
            value = (value << 8) | ord(b)
        values.append((value >> (i & 7)) &~ (0xff << size))
        i = j
    return values

def rotate_data_right(data, steps):
    steps = steps % len(data)
    return data[-steps: ] + data[: -steps]

def rotate_data_left(data, steps):
    steps = steps % len(data)
    return data[steps: ] + data[: steps]

def xor_data(data, key):
    key = key & 0xffffffff
    output = ""
    for c in data:
        key = (key * 279470273) % 4294967291
        output += chr((ord(c) ^ key) & 0xff)
    return output

def wrap_item(is_weapon, values, key):
    item = pack_item_values(is_weapon, values)
    header = struct.pack(">Bi", (is_weapon << 7) | 7, key)
    padding = "\xff" * (33 - len(item))
    h = lzo.crc32(header + "\xff\xff" + item + padding) & 0xffffffff
    checksum = struct.pack(">H", ((h >> 16) ^ h) & 0xffff)
    body = xor_data(rotate_data_left(checksum + item, key & 31), key >> 5)
    return header + body

def unwrap_item(data):
    version_type, key = struct.unpack(">Bi", data[: 5])
    is_weapon = version_type >> 7
    raw = rotate_data_right(xor_data(data[5: ], key >> 5), key & 31)
    return is_weapon, unpack_item_values(is_weapon, raw[2: ]), key


def read_varint(f):
    value = 0
    offset = 0
    while 1:
        b = ord(f.read(1))
        value |= (b & 0x7f) << offset
        if (b & 0x80) == 0:
            break
        offset = offset + 7
    return value

def write_varint(f, i):
    while i > 0x7f:
        f.write(chr(0x80 | (i & 0x7f)))
        i = i >> 7
    f.write(chr(i))

def read_protobuf(data):
    fields = {}
    end_position = len(data)
    bytestream = StringIO(data)
    while bytestream.tell() < end_position:
        key = read_varint(bytestream)
        field_number = key >> 3
        wire_type = key & 7
        value = read_protobuf_value(bytestream, wire_type)
        fields.setdefault(field_number, []).append([wire_type, value])
    return fields

def read_protobuf_value(b, wire_type):
    if wire_type == 0:
        value = read_varint(b)
    elif wire_type == 1:
        value = struct.unpack("<Q", b.read(8))[0]
    elif wire_type == 2:
        length = read_varint(b)
        value = b.read(length)
    elif wire_type == 5:
        value = struct.unpack("<I", b.read(4))[0]
    else:
        raise BL2Error("Unsupported wire type " + str(wire_type))
    return value

def write_protobuf(data):
    b = StringIO()
    # If the data came from a JSON file the keys will all be strings
    data = dict([(int(k), v) for (k, v) in data.items()])
    for key, entries in sorted(data.items()):
        for wire_type, value in entries:
            if type(value) is dict:
                value = write_protobuf(value)
                wire_type = 2
            elif type(value) in (list, tuple):
                sub_b = StringIO()
                for v in value:
                    write_protobuf_value(sub_b, wire_type, v)
                value = sub_b.getvalue()
                wire_type = 2
            write_varint(b, (key << 3) | wire_type)
            write_protobuf_value(b, wire_type, value)
    return b.getvalue()

def write_protobuf_value(b, wire_type, value):
    if wire_type == 0:
        write_varint(b, value)
    elif wire_type == 1:
        b.write(struct.pack("<Q", value))
    elif wire_type == 2:
        if type(value) is unicode:
            value = value.encode("latin1")
        write_varint(b, len(value))
        b.write(value)
    elif wire_type == 5:
        b.write(struct.pack("<I", value))
    else:
        raise BL2Error("Unsupported wire type " + str(wire_type))

def parse_zigzag(i):
    if i & 1:
        return -1 ^ (i >> 1)
    else:
        return i >> 1


def unwrap_player_data(data):
    if data[: 20] != hashlib.sha1(data[20: ]).digest():
        raise BL2Error("Invalid save file")

    data = lzo.decompress("\xf0" + data[20: ])
    size, wsg, version = struct.unpack(">I3sI", data[: 11])
    if version != 2 and version != 0x02000000:
        raise BL2Error("Unknown save version " + str(version))

    if version == 2:
        crc, size = struct.unpack(">II", data[11: 19])
    else:
        crc, size = struct.unpack("<II", data[11: 19])

    bitstream = ReadBitstream(data[19: ])
    tree = read_huffman_tree(bitstream)
    player = huffman_decompress(tree, bitstream, size)

    if (lzo.crc32(player) & 0xffffffff) != crc:
        raise BL2Error("CRC check failed")

    return player

def wrap_player_data(player, endian=1):
    crc = lzo.crc32(player) & 0xffffffff

    bitstream = WriteBitstream()
    tree = make_huffman_tree(player)
    write_huffman_tree(tree, bitstream)
    huffman_compress(invert_tree(tree), player, bitstream)
    data = bitstream.getvalue() + "\x00\x00\x00\x00"

    header = struct.pack(">I3s", len(data) + 15, "WSG")
    if endian == 1:
        header = header + struct.pack(">III", 2, crc, len(player))
    else:
        header = header + struct.pack("<III", 2, crc, len(player))

    data = lzo.compress(header + data)[1: ]

    return hashlib.sha1(data).digest() + data


def modify_save(data, changes, endian=1):
    player = read_protobuf(unwrap_player_data(data))

    if changes.has_key("level"):
        player[2] = [[0, int(changes["level"])]]

    if changes.has_key("skillpoints"):
        player[4] = [[0, int(changes["skillpoints"])]]

    if changes.has_key("money") or changes.has_key("eridium"):
        raw = player[6][0][1]
        b = StringIO(raw)
        values = []
        while b.tell() < len(raw):
            values.append(read_protobuf_value(b, 0))
        if changes.has_key("money"):
            values[0] = int(changes["money"])
        if changes.has_key("eridium"):
            values[1] = int(changes["eridium"])
        player[6][0] = [0, values]

    if changes.has_key("itemlevels"):
        if changes["itemlevels"]:
            level = int(changes["itemlevels"])
        else:
            level = player[2][0][1]
        for field_number in (53, 54):
            for field in player[field_number]:
                field_data = read_protobuf(field[1])
                is_weapon, item, key = unwrap_item(field_data[1][0][1])
                item = item[: 4] + [level, level] + item[6: ]
                field_data[1][0][1] = wrap_item(is_weapon, item, key)
                field[1] = write_protobuf(field_data)

    return wrap_player_data(write_protobuf(player), endian)

def apply_crude_parsing(player, rules):
    for key in rules.split(","):
        if ":" in key:
            key, field_type = key.split(":", 1)
            field_type = int(field_type)
            for element in player.get(int(key), []):
                element[0] = field_type
                b = StringIO(element[1])
                end_position = len(element[1])
                value = []
                while b.tell() < end_position:
                    value.append(read_protobuf_value(b, field_type))
                element[1] = value
        else:
            for element in player.get(int(key), []):
                element[1] = read_protobuf(element[1])

def main():
    usage = "usage: %prog [options] [source file] [destination file]"
    p = optparse.OptionParser()
    p.add_option(
        "-d", "--decode",
        action="store_true",
        help="read from a save game, rather than creating one"
    )
    p.add_option(
        "-j", "--json",
        action="store_true",
        help="read or write save game data in JSON format, rather than raw protobufs"
    )
    p.add_option(
        "-l", "--little-endian",
        action="store_true",
        help="change the output format to little endian, to write PC-compatible save files"
    )
    p.add_option(
        "-m", "--modify", metavar="MODIFICATIONS",
        help="comma separated list of modifications to make, eg money=99999999,eridium=99"
    )
    p.add_option(
        "-p", "--parse", metavar="FIELDNUMS",
        help="perform further protobuf parsing on the specified comma separated list of keys"
    )
    options, args = p.parse_args()

    if len(args) < 1 or args[0] == "-":
        input = sys.stdin
    else:
        input = open(args[0], "rb")

    if len(args) < 2 or args[1] == "-":
        output = sys.stdout
    else:
        output = open(args[1], "wb")

    if options.little_endian:
        endian = 0
    else:
        endian = 1

    if options.modify is not None:
        changes = {}
        if options.modify:
            for m in options.modify.split(","):
                k, v = (m.split("=", 1) + [None])[: 2]
                changes[k] = v
        output.write(modify_save(input.read(), changes, endian))
    elif options.decode:
        savegame = input.read()
        player = unwrap_player_data(savegame)
        if options.json:
            player = read_protobuf(player)
            if options.parse:
                apply_crude_parsing(player, options.parse)
            player = json.dumps(player, encoding="latin1", sort_keys=True, indent=4)
        output.write(player)
    else:
        player = input.read()
        if options.json:
            player = write_protobuf(json.loads(player, encoding="latin1"))
        savegame = wrap_player_data(player, endian)
        output.write(savegame)

if __name__ == "__main__":
    main()
