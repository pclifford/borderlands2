import io
import struct
from typing import Any

from borderlands.datautil.common import wrap_bytes, guess_wire_type
from borderlands.datautil.data_types import PlayerDict
from borderlands.datautil.errors import BorderlandsError


def remove_structure(data: dict, inv: dict) -> dict:
    result = {}
    result.update(data.get("_raw", {}))
    for k, value in data.items():
        if k == "_raw":
            # Fix for Python 3 - these inner lists need to be
            # run through wrap_bytes, else they'll be interpreted
            # weirdly.
            for raw_k, raw_values in value.items():
                for idx, (wire_type, v) in enumerate(raw_values):
                    if wire_type == 2:
                        raw_values[idx][1] = wrap_bytes(v)
            continue
        mapping = inv.get(k)
        if mapping is None:
            raise BorderlandsError(f"Unknown key {k!r} in data")
        elif isinstance(mapping, int):
            result[mapping] = [[guess_wire_type(value), value]]
            continue
        key, repeated, child_inv = mapping
        if child_inv is None:
            value = [value] if not repeated else value
            result[key] = [[guess_wire_type(v), v] for v in value]
        elif isinstance(child_inv, int):
            if repeated:
                b = io.BytesIO()
                for v in value:
                    write_protobuf_value(b=b, wire_type=child_inv, value=v)
                result[key] = [[2, b.getvalue()]]
            else:
                result[key] = [[child_inv, value]]
        elif isinstance(child_inv, tuple):
            if not repeated:
                value = [value]
            values = []
            for v in map(child_inv[1], value):
                if isinstance(v, list):
                    values.append(v)
                else:
                    values.append([guess_wire_type(v), v])
            result[key] = values
        elif isinstance(child_inv, dict):
            value = [value] if not repeated else value
            values = []
            for d in [remove_structure(v, child_inv) for v in value]:
                values.append([2, write_protobuf(d)])
            result[key] = values
        else:
            raise Exception(f"Invalid mapping {mapping!r} for {k!r}: {value!r}")
    return result


def read_varint(f: io.BytesIO) -> int:
    value = 0
    offset = 0
    while True:
        b = ord(f.read(1))
        value |= (b & 0x7F) << offset
        if (b & 0x80) == 0:
            break
        offset = offset + 7
    return value


def write_varint(f: io.BytesIO, i: int) -> None:
    while i > 0x7F:
        f.write(bytes([0x80 | (i & 0x7F)]))
        i = i >> 7
    f.write(bytes([i]))


def read_protobuf_value(b: io.BytesIO, wire_type: int) -> Any:
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
        raise BorderlandsError("Unsupported wire type " + str(wire_type))
    return value


def read_repeated_protobuf_value(data: bytes, wire_type: int) -> list:
    b = io.BytesIO(data)
    values = []
    while b.tell() < len(data):
        values.append(read_protobuf_value(b, wire_type))
    return values


def write_protobuf_value(*, b: io.BytesIO, wire_type: int, value: Any) -> None:
    if wire_type == 0:
        write_varint(b, value)
    elif wire_type == 1:
        b.write(struct.pack("<Q", value))
    elif wire_type == 2:
        if isinstance(value, str):
            value = value.encode('latin1')
        elif isinstance(value, list):
            value = "".join(map(chr, value)).encode('latin1')
        write_varint(b, len(value))
        b.write(value)
    elif wire_type == 5:
        b.write(struct.pack("<I", value))
    else:
        raise BorderlandsError(f"Unsupported wire type {wire_type}")


def write_repeated_protobuf_value(data: list, wire_type: int) -> bytes:
    b = io.BytesIO()
    for value in data:
        write_protobuf_value(b=b, wire_type=wire_type, value=value)
    return b.getvalue()


def read_protobuf(data: bytes) -> PlayerDict:
    fields = {}
    end_position = len(data)
    bytestream = io.BytesIO(data)
    while bytestream.tell() < end_position:
        key = read_varint(bytestream)
        field_number = key >> 3
        wire_type = key & 7
        value = read_protobuf_value(bytestream, wire_type)
        fields.setdefault(field_number, []).append([wire_type, value])
    return fields


def apply_structure(pb_data: PlayerDict, s: dict) -> dict:
    fields = {}
    raw = {}
    for k, data in pb_data.items():
        mapping = s.get(k)
        if mapping is None:
            raw[k] = data
            continue
        elif isinstance(mapping, str):
            fields[mapping] = data[0][1]
            continue
        key, repeated, child_s = mapping
        if child_s is None:
            values = [d[1] for d in data]
            fields[key] = values if repeated else values[0]
        elif isinstance(child_s, int):
            if repeated:
                fields[key] = read_repeated_protobuf_value(data[0][1], child_s)
            else:
                fields[key] = data[0][1]
        elif isinstance(child_s, tuple):
            values = [child_s[0](d[1]) for d in data]
            fields[key] = values if repeated else values[0]
        elif isinstance(child_s, dict):
            values = [apply_structure(read_protobuf(d[1]), child_s) for d in data]
            fields[key] = values if repeated else values[0]
        else:
            raise TypeError(f"Wrong type of child_s: {type(child_s)}. Invalid mapping {mapping!r} for {k!r}: {data!r}")
    if len(raw) != 0:
        fields["_raw"] = {}
        for k, values in raw.items():
            safe_values = []
            for wire_type, v in values:
                if wire_type == 2:
                    v = list(v)
                safe_values.append([wire_type, v])
            fields["_raw"][k] = safe_values
    return fields


def write_protobuf(data: dict) -> bytes:
    b = io.BytesIO()
    # If the data came from a JSON file the keys will all be strings
    data = {int(k): v for k, v in data.items()}
    for key, entries in sorted(data.items()):
        for wire_type, value in entries:
            if isinstance(value, dict):
                value = write_protobuf(value)
                wire_type = 2
            elif isinstance(value, (list, tuple)) and wire_type != 2:
                sub_b = io.BytesIO()
                for v in value:
                    write_protobuf_value(b=sub_b, wire_type=wire_type, value=v)
                value = sub_b.getvalue()
                wire_type = 2
            write_varint(b, (key << 3) | wire_type)
            write_protobuf_value(b=b, wire_type=wire_type, value=value)
    return b.getvalue()
