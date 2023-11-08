import sys
from typing import Final, Optional, Tuple

CLZ_TABLE: Final = (
    32,
    0,
    1,
    26,
    2,
    23,
    27,
    0,
    3,
    16,
    24,
    30,
    28,
    11,
    0,
    13,
    4,
    7,
    17,
    0,
    25,
    22,
    31,
    15,
    29,
    10,
    12,
    6,
    0,
    21,
    14,
    9,
    5,
    20,
    8,
    19,
    18,
)


def expand_zeroes(*, src: bytearray, ip: int, extra: int) -> Tuple[int, int]:
    start = ip
    # TODO: add check for src.size
    while src[ip] == 0:
        ip = ip + 1
    v = ((ip - start) * 255) + src[ip]
    return v + extra, ip + 1


def copy_earlier(*, b: bytearray, offset: int, chunk_size: int) -> None:
    i = len(b) - offset
    end = i + chunk_size
    while i < end:
        chunk = b[i : i + chunk_size]
        i = i + len(chunk)
        chunk_size = chunk_size - len(chunk)
        b.extend(chunk)


def read_xor32(src: bytearray, p1: int, p2: int) -> int:
    v1 = src[p1] | (src[p1 + 1] << 8) | (src[p1 + 2] << 16) | (src[p1 + 3] << 24)
    v2 = src[p2] | (src[p2 + 1] << 8) | (src[p2 + 2] << 16) | (src[p2 + 3] << 24)
    return v1 ^ v2


def lzo1x_decompress(s: bytes) -> bytes:
    dst = bytearray()
    src = bytearray(s)
    ip = 5

    t = src[ip]
    ip += 1
    if t > 17:
        t = t - 17
        dst.extend(src[ip : ip + t])
        ip += t
        t = src[ip]
        ip += 1
    elif t < 16:
        if t == 0:
            t, ip = expand_zeroes(src=src, ip=ip, extra=15)
        dst.extend(src[ip : ip + t + 3])
        ip += t + 3
        t = src[ip]
        ip += 1

    while True:
        while True:
            if t >= 64:
                copy_earlier(b=dst, offset=1 + ((t >> 2) & 7) + (src[ip] << 3), chunk_size=(t >> 5) + 1)
                ip += 1
            elif t >= 32:
                count = t & 31
                if count == 0:
                    count, ip = expand_zeroes(src=src, ip=ip, extra=31)
                t = src[ip]
                copy_earlier(b=dst, offset=1 + ((t | (src[ip + 1] << 8)) >> 2), chunk_size=count + 2)
                ip += 2
            elif t >= 16:
                offset = (t & 8) << 11
                count = t & 7
                if count == 0:
                    count, ip = expand_zeroes(src=src, ip=ip, extra=7)
                t = src[ip]
                offset += (t | (src[ip + 1] << 8)) >> 2
                ip += 2
                if offset == 0:
                    return bytes(dst)
                copy_earlier(b=dst, offset=offset + 0x4000, chunk_size=count + 2)
            else:
                copy_earlier(b=dst, offset=1 + (t >> 2) + (src[ip] << 2), chunk_size=2)
                ip += 1

            t = t & 3
            if t == 0:
                break
            dst.extend(src[ip : ip + t])
            ip += t
            t = src[ip]
            ip += 1

        while True:
            t = src[ip]
            ip += 1
            if t < 16:
                if t == 0:
                    t, ip = expand_zeroes(src=src, ip=ip, extra=15)
                dst.extend(src[ip : ip + t + 3])
                ip += t + 3
                t = src[ip]
                ip += 1
            if t < 16:
                copy_earlier(b=dst, offset=1 + 0x0800 + (t >> 2) + (src[ip] << 2), chunk_size=3)
                ip += 1
                t = t & 3
                if t == 0:
                    continue
                dst.extend(src[ip : ip + t])
                ip += t
                t = src[ip]
                ip += 1
            break


def lzo1x_1_compress_core(*, src: bytearray, dst: bytearray, ti: int, ip_start: int, ip_len: int) -> Optional[int]:
    dict_entries = [0] * 16384

    in_end = ip_start + ip_len
    ip_end = ip_start + ip_len - 20

    ip = ip_start
    ii = ip_start

    ip += (4 - ti) if ti < 4 else 0
    ip += 1 + ((ip - ii) >> 5)
    while True:
        while True:
            if ip >= ip_end:
                return in_end - (ii - ti)
            dv = src[ip : ip + 4]
            dindex = dv[0] | (dv[1] << 8) | (dv[2] << 16) | (dv[3] << 24)
            dindex = ((0x1824429D * dindex) >> 18) & 0x3FFF
            m_pos = ip_start + dict_entries[dindex]
            dict_entries[dindex] = (ip - ip_start) & 0xFFFF
            if dv == src[m_pos : m_pos + 4]:
                break
            ip += 1 + ((ip - ii) >> 5)

        ii -= ti
        ti = 0
        t = ip - ii
        if t != 0:
            if t <= 3:
                dst[-2] |= t
                dst.extend(src[ii : ii + t])
            elif t <= 16:
                dst.append(t - 3)
                dst.extend(src[ii : ii + t])
            else:
                if t <= 18:
                    dst.append(t - 3)
                else:
                    tt = t - 18
                    dst.append(0)
                    n, tt = divmod(tt, 255)
                    dst.extend(b"\x00" * n)
                    dst.append(tt)
                dst.extend(src[ii : ii + t])
                ii += t

        m_len = 4
        v = read_xor32(src, ip + m_len, m_pos + m_len)
        if v == 0:
            while True:
                m_len += 4
                v = read_xor32(src, ip + m_len, m_pos + m_len)
                if ip + m_len >= ip_end:
                    break
                elif v != 0:
                    m_len += CLZ_TABLE[(v & -v) % 37] >> 3
                    break
        else:
            m_len += CLZ_TABLE[(v & -v) % 37] >> 3

        m_off = ip - m_pos
        ip += m_len
        ii = ip
        if m_len <= 8 and m_off <= 0x0800:
            m_off -= 1
            dst.append(((m_len - 1) << 5) | ((m_off & 7) << 2))
            dst.append(m_off >> 3)
        elif m_off <= 0x4000:
            m_off -= 1
            if m_len <= 33:
                dst.append(32 | (m_len - 2))
            else:
                m_len -= 33
                dst.append(32)
                n, m_len = divmod(m_len, 255)
                dst.extend(b"\x00" * n)
                dst.append(m_len)
            dst.append((m_off << 2) & 0xFF)
            dst.append((m_off >> 6) & 0xFF)
        else:
            m_off -= 0x4000
            if m_len <= 9:
                dst.append(0xFF & (16 | ((m_off >> 11) & 8) | (m_len - 2)))
            else:
                m_len -= 9
                dst.append(0xFF & (16 | ((m_off >> 11) & 8)))
                n, m_len = divmod(m_len, 255)
                dst.extend(b"\x00" * n)
                dst.append(m_len)
            dst.append((m_off << 2) & 0xFF)
            dst.append((m_off >> 6) & 0xFF)


def lzo1x_1_compress(s: bytes) -> bytes:
    src = bytearray(s)
    dst = bytearray()

    ip = 0
    len_ = len(s)
    t = 0

    dst.append(240)
    dst.append((len_ >> 24) & 0xFF)
    dst.append((len_ >> 16) & 0xFF)
    dst.append((len_ >> 8) & 0xFF)
    dst.append(len_ & 0xFF)

    while len_ > 20 and t + len_ > 31:
        ll = min(49152, len_)
        temp = lzo1x_1_compress_core(src=src, dst=dst, ti=t, ip_start=ip, ip_len=ll)
        if temp is None:
            sys.exit('None from lzo1x_1_compress_core')
        t = temp
        ip += ll
        len_ -= ll
    t += len_

    if t > 0:
        ii = len(s) - t

        if len(dst) == 5 and t <= 238:
            dst.append(17 + t)
        elif t <= 3:
            dst[-2] |= t
        elif t <= 18:
            dst.append(t - 3)
        else:
            tt = t - 18
            dst.append(0)
            n, tt = divmod(tt, 255)
            dst.extend(b"\x00" * n)
            dst.append(tt)
        dst.extend(src[ii : ii + t])

    dst.append(16 | 1)
    dst.append(0)
    dst.append(0)

    return bytes(dst)
