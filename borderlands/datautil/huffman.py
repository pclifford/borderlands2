from bisect import insort

from borderlands.datautil.bitstreams import ReadBitstream, WriteBitstream


class HuffmanNode:
    """
    This is a bit of a hack because I don't feel like rewriting `make_huffman_tree`
    entirely.  Basically the current implementation relies on Python 2 behavior
    where lists and ints can be compared directly with comparison operators.
    Python 3 forbids this, so the call to `bisect.insort()` inside
    `make_huffman_tree` fails once it encounters a "regular" two-element list
    with two ints, and another whose second element is a nested structure.
    Really `make_huffman_tree` should just be rewritten to be sensible, but
    rather than doing that I'm doing this hacky thing.  C'est la vie.
    """

    def __init__(self, *, weight: int, data) -> None:
        self.weight = weight
        self.data = data

    def __repr__(self) -> str:
        return f'hn({self.weight}, {self.data})'

    def __lt__(self, other) -> bool:
        """
        Compare by weight, and then by data.  If the data on either
        isn't an int, sort it after the other one (as Python 2
        would do)
        """
        if self.weight != other.weight:
            return self.weight < other.weight

        if isinstance(self.data, int) and isinstance(other.data, int):
            return self.data < other.data
        else:
            return isinstance(self.data, int)

    def to_list(self) -> list:
        """
        Returns ourselves as a nested collection of lists, rather than a
        nested collection of HuffmanNodes.
        """
        if isinstance(self.data, int):
            return [self.weight, self.data]
        else:
            return [self.weight, [d.to_list() for d in self.data]]


def read_huffman_tree(b: ReadBitstream):
    node_type = b.read_bit()
    if node_type == 0:
        return None, (read_huffman_tree(b), read_huffman_tree(b))
    else:
        return None, b.read_byte()


def write_huffman_tree(node, b: WriteBitstream) -> None:
    if isinstance(node[1], int):
        b.write_bit(1)
        b.write_byte(node[1])
    else:
        b.write_bit(0)
        write_huffman_tree(node[1][0], b)
        write_huffman_tree(node[1][1], b)


def make_huffman_tree(data) -> list:
    frequencies = [0] * 256
    for c in data:
        frequencies[c] += 1

    nodes = [HuffmanNode(weight=f, data=i) for i, f in enumerate(frequencies) if f != 0]
    nodes.sort()

    while len(nodes) > 1:
        left, right = nodes[:2]
        nodes = nodes[2:]
        insort(nodes, HuffmanNode(weight=left.weight + right.weight, data=[left, right]))

    return nodes[0].to_list()


def invert_tree(node, code=0, bits=0) -> dict:
    if isinstance(node[1], int):
        return {node[1]: (code, bits)}
    else:
        result = {}
        result.update(invert_tree(node[1][0], code << 1, bits + 1))
        result.update(invert_tree(node[1][1], (code << 1) | 1, bits + 1))
        return result


def huffman_decompress(tree, bitstream, size) -> bytes:
    output = bytearray()
    while len(output) < size:
        node = tree
        while True:
            b = bitstream.read_bit()
            node = node[1][b]
            if isinstance(node[1], int):
                output.append(node[1])
                break
    return bytes(output)


def huffman_compress(encoding, data, bitstream):
    for c in data:
        code, nbits = encoding[c]
        bitstream.write_bits(code, nbits)
