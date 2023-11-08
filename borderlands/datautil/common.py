import binascii
import struct
from typing import Any, Union, List, Dict


def wrap_float(v: float) -> List[Union[int, Any]]:
    return [5, struct.unpack("<I", struct.pack("<f", v))[0]]


def unwrap_float(v: Any) -> float:
    return struct.unpack("<f", struct.pack("<I", v))[0]


def unwrap_bytes(value: bytes) -> list:
    return list(value)


def wrap_bytes(value: list) -> bytes:
    return bytes(value)


def guess_wire_type(value: Any) -> int:
    if isinstance(value, (str, bytes)):
        return 2
    else:
        return 0


def invert_structure(structure: dict) -> dict:
    inv: Dict[Any, tuple] = {}
    for k, v in structure.items():
        if isinstance(v, tuple):
            if isinstance(v[2], dict):  # TODO: check len(v)
                inv[v[0]] = (k, v[1], invert_structure(v[2]))
            else:
                inv[v[0]] = (k,) + v[1:]
        else:
            inv[v] = k
    return inv


def conv_binary_to_str(data: Any) -> Any:
    """
    In Python 2, we can dump to a JSON object directly, but Python 3
    doesn't like that some of the data is binary (since that's invalid in
    JSON).  Python 2 would just cast those as strings automatically.
    So this will loop through and convert everything that's binary
    into a string.
    """
    if isinstance(data, bytes):
        return data.decode('latin1')
    elif isinstance(data, dict):
        return {k: conv_binary_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [conv_binary_to_str(x) for x in data]
    else:
        return data


def rotate_data_right(data: bytes, steps: int) -> bytes:
    steps = steps % len(data)
    return data[-steps:] + data[:-steps]


def rotate_data_left(data: bytes, steps: int) -> bytes:
    steps = steps % len(data)
    return data[steps:] + data[:steps]


def xor_data(data, key: int) -> bytes:
    key = key & 0xFFFFFFFF
    output = bytearray()
    for c in data:
        key = (key * 279470273) % 4294967291
        output.append((c ^ key) & 0xFF)
    return bytes(output)


def create_body(*, item: bytes, header: bytes, key: int) -> bytes:
    padding = b"\xff" * (33 - len(item))
    h = binascii.crc32(header + b"\xff\xff" + item + padding) & 0xFFFFFFFF
    checksum = struct.pack(">H", ((h >> 16) ^ h) & 0xFFFF)
    body = xor_data(rotate_data_left(checksum + item, key & 31), key >> 5)
    return body


def replace_raw_item_key(data: bytes, key: int) -> bytes:
    old_key = struct.unpack(">i", data[1:5])[0]
    item = rotate_data_right(xor_data(data[5:], old_key >> 5), old_key & 31)[2:]
    header = struct.pack(">Bi", data[0], key)
    return header + create_body(item=item, header=header, key=key)
