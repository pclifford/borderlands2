import argparse
import base64
import binascii
import dataclasses
import hashlib
import io
import json
import math
import os
import random
import struct
import sys
from typing import List, Tuple, Dict, Any, Optional, IO, Union

from borderlands.challenges import Challenge, unwrap_challenges, wrap_challenges
from borderlands.config import parse_args
from borderlands.datautil.bitstreams import ReadBitstream, WriteBitstream
from borderlands.datautil.common import conv_binary_to_str, rotate_data_right, xor_data, create_body
from borderlands.datautil.common import invert_structure, replace_raw_item_key
from borderlands.datautil.data_types import PlayerDict
from borderlands.datautil.errors import BorderlandsError
from borderlands.datautil.huffman import (
    read_huffman_tree,
    make_huffman_tree,
    write_huffman_tree,
    invert_tree,
    huffman_decompress,
    huffman_compress,
)
from borderlands.datautil.lzo1x import lzo1x_decompress, lzo1x_1_compress
from borderlands.datautil.protobuf import (
    read_protobuf_value,
    read_repeated_protobuf_value,
    write_repeated_protobuf_value,
    read_protobuf,
    apply_structure,
    write_protobuf,
    remove_structure,
)


@dataclasses.dataclass(frozen=True)
class InputFileData:
    filename: str
    filehandle: IO
    close: bool


class BaseApp:
    """
    Base application class.
    """

    # These seem to be the same for both BL2 and BLTPS
    item_sizes = (
        (8, 17, 20, 11, 7, 7, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16),
        (8, 13, 20, 11, 7, 7, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17),
    )

    # Ditto
    item_header_sizes = (
        (("type", 8), ("balance", 10), ("manufacturer", 7)),
        (("type", 6), ("balance", 10), ("manufacturer", 7)),
    )

    min_backpack_size = 12
    max_backpack_size = 39
    min_bank_size = 6
    max_bank_size = 24

    # "laser" in here doesn't apply to BL2, but it won't hurt anything
    # because we process ammo pools based off the black market values,
    # which won't include lasers for BL2
    ammo_resources: Dict[str, Tuple[str, str]] = {
        'rifle': ('D_Resources.AmmoResources.Ammo_Combat_Rifle', 'D_Resourcepools.AmmoPools.Ammo_Combat_Rifle_Pool'),
        'shotgun': (
            'D_Resources.AmmoResources.Ammo_Combat_Shotgun',
            'D_Resourcepools.AmmoPools.Ammo_Combat_Shotgun_Pool',
        ),
        'grenade': (
            'D_Resources.AmmoResources.Ammo_Grenade_Protean',
            'D_Resourcepools.AmmoPools.Ammo_Grenade_Protean_Pool',
        ),
        'smg': ('D_Resources.AmmoResources.Ammo_Patrol_SMG', 'D_Resourcepools.AmmoPools.Ammo_Patrol_SMG_Pool'),
        'pistol': (
            'D_Resources.AmmoResources.Ammo_Repeater_Pistol',
            'D_Resourcepools.AmmoPools.Ammo_Repeater_Pistol_Pool',
        ),
        'launcher': (
            'D_Resources.AmmoResources.Ammo_Rocket_Launcher',
            'D_Resourcepools.AmmoPools.Ammo_Rocket_Launcher_Pool',
        ),
        'sniper': ('D_Resources.AmmoResources.Ammo_Sniper_Rifle', 'D_Resourcepools.AmmoPools.Ammo_Sniper_Rifle_Pool'),
        'laser': ('D_Resources.AmmoResources.Ammo_Combat_Laser', 'D_Resourcepools.AmmoPools.Ammo_Combat_Laser_Pool'),
    }

    # An equation for computing the XP required for a given level is
    # stated at http://borderlands.wikia.com/wiki/Experience_Points to
    # be (in Python terms):
    #
    #       math.ceil(60*(level**2.8) - 60)
    #
    # That works well for most of the levels in the game but it's not
    # perfect - it overshoots a bit towards the higher levels, which can
    # result in some annoying error messages in the game if you bring
    # a character to level 72 but have slightly too much XP.  Changing
    # math.ceil() to plain ol' int() works a bit better for that, actually.
    # Things get a bit better in Python if we use decimal.Decimal for
    # the numbers instead of relying on Python's native floats, but even
    # then it's not perfect.  I've tried out the calculation for level
    # 72 on a few different languages/calculators/platforms, and I think
    # the equation is just not exactly correct.
    #
    # So, what the heck - we'll just hardcode the XP requirements in here.
    #
    # Update in 2023, btw: I'd looked into this more thoroughly because
    # it's the same essential math used in BL3 / Wonderlands (including
    # Chaos XP in WL), and I was having the same XP drift over there that
    # I'd always seen while trying to compute this stuff in Python.  Well,
    # it turns out that the essential problem is that Python sort of
    # unavoidably does all the calculations using 64-bit doubles, instead
    # of 32-bit floats.  The difference in precision starts to add up over
    # time.  It turns out to be *real* difficult to force Python to use
    # floats in the background; you've gotta start doing stuff like `ctypes`
    # shenanigans to even have a prayer of it, and even then it's tricky
    # and might even require custom C extensions.  Anyway, I feel quite good
    # about these hardcodes.  Not worth the trouble in here, for sure.
    required_xp = [
        0,  # lvl 1
        358,  # lvl 2
        1241,  # lvl 3
        2850,  # lvl 4
        5376,  # lvl 5
        8997,  # lvl 6
        13886,  # lvl 7
        20208,  # lvl 8
        28126,  # lvl 9
        37798,  # lvl 10
        49377,  # lvl 11
        63016,  # lvl 12
        78861,  # lvl 13
        97061,  # lvl 14
        117757,  # lvl 15
        141092,  # lvl 16
        167206,  # lvl 17
        196238,  # lvl 18
        228322,  # lvl 19
        263595,  # lvl 20
        302190,  # lvl 21
        344238,  # lvl 22
        389873,  # lvl 23
        439222,  # lvl 24
        492414,  # lvl 25
        549578,  # lvl 26
        610840,  # lvl 27
        676325,  # lvl 28
        746158,  # lvl 29
        820463,  # lvl 30
        899363,  # lvl 31
        982980,  # lvl 32
        1071435,  # lvl 33
        1164850,  # lvl 34
        1263343,  # lvl 35
        1367034,  # lvl 36
        1476041,  # lvl 37
        1590483,  # lvl 38
        1710476,  # lvl 39
        1836137,  # lvl 40
        1967582,  # lvl 41
        2104926,  # lvl 42
        2248285,  # lvl 43
        2397772,  # lvl 44
        2553501,  # lvl 45
        2715586,  # lvl 46
        2884139,  # lvl 47
        3059273,  # lvl 48
        3241098,  # lvl 49
        3429728,  # lvl 50
        3625271,  # lvl 51
        3827840,  # lvl 52
        4037543,  # lvl 53
        4254491,  # lvl 54
        4478792,  # lvl 55
        4710556,  # lvl 56
        4949890,  # lvl 57
        5196902,  # lvl 58
        5451701,  # lvl 59
        5714393,  # lvl 60
        5985086,  # lvl 61
        6263885,  # lvl 62
        6550897,  # lvl 63
        6846227,  # lvl 64
        7149982,  # lvl 65
        7462266,  # lvl 66
        7783184,  # lvl 67
        8112840,  # lvl 68
        8451340,  # lvl 69
        8798786,  # lvl 70
        9155282,  # lvl 71
        9520931,  # lvl 72
        9895837,  # lvl 73
        10280103,  # lvl 74
        10673830,  # lvl 75
        11077120,  # lvl 76
        11490077,  # lvl 77
        11912801,  # lvl 78
        12345393,  # lvl 79
        12787955,  # lvl 80
    ]

    def __init__(
        self,
        *,
        args: List[str],
        item_struct_version: int,
        game_name: str,
        item_prefix: str,
        max_level: int,  # Max char level
        black_market_keys: Tuple[str, ...],
        black_market_ammo: Dict[str, List[int]],
        unlock_choices: List[str],  # Available choices for --unlock option
        challenges: Dict[int, Challenge],
    ) -> None:
        # B2 version is 7, TPS version is 10
        # "version" taken from what Gibbed calls it, not sure if that's
        # an appropriate descriptor or not.
        self.item_struct_version = item_struct_version

        # Item export/import prefix
        self.item_prefix = item_prefix

        # The only difference here is that BLTPS has "laser"
        self.black_market_keys = black_market_keys

        # Dict to tell us which black market keys are ammo-related, and
        # what the max ammo is at each level.  Could be computed pretty
        # easily, but we may as well just store it.
        self.black_market_ammo = black_market_ammo

        # There are two possible ways of uniquely identifying challenges in this file:
        # via their numeric position in the list, or by what looks like an internal
        # ID (though that ID is constructed a little weirdly, so I'm not sure if it's
        # actually intended to be used that way or not).
        #
        # I did run some tests, and it looks like internally, B2 probably does use
        # that ID field to identify the challenges...  You can mess around with the
        # order in which they're saved to the file, but so long as the ID field
        # is still pointing to the challenge you want, it'll be read in properly
        # (and then when you save your game, they'll be written back out in the
        # original order).
        #
        # Given that, I decided to go ahead and use that probably-ID field as the
        # index on this dict, rather than the order.  That should be slightly more
        # flexible for anyone editing the JSON directly, and theoretically
        # shouldn't be a problem in the future since there won't be any new major
        # DLC for B2...
        #
        # New major DLC for TPS seems unlikely too, though time will tell.
        self.challenges = challenges

        # Set up a reverse lookup for our ammo pools
        self.ammo_resource_lookup = {}
        for shortname, (resource, pool) in self.ammo_resources.items():
            self.ammo_resource_lookup[resource] = shortname

        # Parse Arguments
        self.config = parse_args(
            args=args,
            setup_currency_args=self.setup_currency_args,
            setup_game_specific_args=self.setup_game_specific_args,
            game_name=game_name,
            max_level=max_level,
            min_backpack_size=self.min_backpack_size,
            max_backpack_size=self.max_backpack_size,
            min_bank_size=self.min_bank_size,
            max_bank_size=self.max_bank_size,
            unlock_choices=unlock_choices,
        )

        # Sets up our main save_structure var which controls how we read the file
        # This is implemented in AppBL2 and AppBLTPS
        self.save_structure = self.create_save_structure()

    def pack_item_values(self, is_weapon: int, values: list) -> bytes:
        i = 0
        item_bytes = bytearray(32)
        for value, size in zip(values, self.item_sizes[is_weapon]):
            if value is None:
                break
            j = i >> 3
            value = value << (i & 7)
            while value != 0:
                item_bytes[j] |= value & 0xFF
                value = value >> 8
                j = j + 1
            i = i + size
        if (i & 7) != 0:
            value = 0xFF << (i & 7)
            item_bytes[i >> 3] |= value & 0xFF
        return bytes(item_bytes[: (i + 7) >> 3])

    def unpack_item_values(self, is_weapon: int, data: bytes) -> List[Optional[int]]:
        i = 8
        data = b' ' + data
        end = len(data) * 8
        result: List[Optional[int]] = []
        for size in self.item_sizes[is_weapon]:
            j = i + size
            if j > end:
                result.append(None)
                continue
            value = 0
            for b in data[j >> 3 : (i >> 3) - 1 : -1]:
                value = (value << 8) | b
            result.append((value >> (i & 7)) & ~(0xFF << size))
            i = j
        return result

    def wrap_item(self, *, is_weapon: int, values: list, key: int) -> bytes:
        item = self.pack_item_values(is_weapon, values)
        header = struct.pack(">Bi", (is_weapon << 7) | self.item_struct_version, key)
        return header + create_body(item=item, header=header, key=key)

    def unwrap_item(self, data: bytes) -> Tuple[int, List[Optional[int]], int]:
        version_type, key = struct.unpack(">Bi", data[:5])
        is_weapon = version_type >> 7
        raw = rotate_data_right(xor_data(data[5:], key >> 5), key & 31)
        return is_weapon, self.unpack_item_values(is_weapon, raw[2:]), key

    def unwrap_black_market(self, value: bytes) -> dict:
        sdu_list = read_repeated_protobuf_value(value, 0)
        return dict(zip(self.black_market_keys, sdu_list))

    def wrap_black_market(self, value: dict) -> bytes:
        sdu_list = [value[k] for k in self.black_market_keys[: len(value)]]
        return write_repeated_protobuf_value(sdu_list, 0)

    def unwrap_challenges(self, data: bytes) -> dict:
        return unwrap_challenges(data=data, challenges=self.challenges, endian=self.config.endian)

    def wrap_challenges(self, data: dict) -> bytes:
        return wrap_challenges(data=data, endian=self.config.endian)

    def unwrap_item_info(self, value: bytes) -> dict:
        is_weapon, item, key = self.unwrap_item(value)

        data: Dict[str, Any] = {
            'is_weapon': is_weapon,
            'key': key,
            'set': item[0],
            'level': (item[4], item[5]),  # (grade_index, game_stage)
            '_base64': base64.b64encode(value),
        }
        for i, (k, bits) in enumerate(self.item_header_sizes[is_weapon]):
            x = item[1 + i]
            if x is None:
                sys.exit('unwrap_item_info got None instead of int')
            lib = x >> bits
            asset = x & ~(lib << bits)
            data[k] = {"lib": lib, "asset": asset}
        bits = 10 + is_weapon
        parts: List[Optional[Dict[str, Any]]] = []
        for x in item[6:]:
            if x is None:
                parts.append(None)
            else:
                lib = x >> bits
                asset = x & ~(lib << bits)
                parts.append({"lib": lib, "asset": asset})
        data["parts"] = parts
        return data

    def wrap_item_info(self, value: dict) -> bytes:
        parts = [value["set"]]
        for key, bits in self.item_header_sizes[value["is_weapon"]]:
            v = value[key]
            parts.append((v["lib"] << bits) | v["asset"])
        parts.extend(value["level"])  # (grade_index, game_stage)
        bits = 10 + value["is_weapon"]
        for v in value["parts"]:
            if v is None:
                parts.append(None)
            else:
                parts.append((v["lib"] << bits) | v["asset"])
        return self.wrap_item(is_weapon=value["is_weapon"], values=parts, key=value["key"])

    @staticmethod
    def unwrap_player_data(data: bytes) -> bytes:
        """
        Byte order on the few struct calls here appears to actually be
        hardcoded regardless of platform, so we're perhaps just leaving
        them, rather than using self.config.endian as we're doing elsewhere.
        I suspect this might actually be wrong, though, and just happens to
        work.
        """
        if data[:4] == "CON ":
            raise BorderlandsError(
                "You need to use a program like Horizon or Modio to extract the SaveGame.sav file first"
            )

        if data[:20] != hashlib.sha1(data[20:]).digest():
            raise BorderlandsError("Invalid save file")

        data = lzo1x_decompress(b'\xf0' + data[20:])
        size, wsg, version = struct.unpack('>I3sI', data[:11])
        if version != 2 and version != 0x02000000:
            raise BorderlandsError(f'Unknown save version {version}')

        if version == 2:
            crc, size = struct.unpack(">II", data[11:19])
        else:
            crc, size = struct.unpack("<II", data[11:19])

        bitstream = ReadBitstream(data[19:])
        tree = read_huffman_tree(bitstream)
        player = huffman_decompress(tree, bitstream, size)

        if (binascii.crc32(player) & 0xFFFFFFFF) != crc:
            raise BorderlandsError("CRC check failed")

        return player

    def wrap_player_data(self, player: bytes) -> bytes:
        """
        There's one call in here which had a hard-coded endian, as with
        unwrap_player_data above, so we're leaving that hardcoded for now.
        I suspect that it's wrong to be doing so, though.
        """
        crc = binascii.crc32(player) & 0xFFFFFFFF

        bitstream = WriteBitstream()
        tree = make_huffman_tree(player)
        write_huffman_tree(tree, bitstream)
        huffman_compress(invert_tree(tree), player, bitstream)
        data = bitstream.getvalue() + b"\x00\x00\x00\x00"

        header = struct.pack(">I3s", len(data) + 15, b'WSG')
        header += struct.pack(self.config.endian + "III", 2, crc, len(player))

        data = lzo1x_1_compress(header + data)[1:]

        return hashlib.sha1(data).digest() + data

    def show_save_info(self, data: bytes) -> None:
        """
        Shows information from file data, based on our config object.
        "data" should be the raw data from a save file.

        Note that if a user is both showing info and making changes,
        we're parsing the protobuf twice, since modify_save also does
        that.  Inefficiency!
        """
        player = read_protobuf(self.unwrap_player_data(data))
        self._show_save_info(player)

    def _show_save_info(self, player: PlayerDict) -> None:
        if self.config.print_unexplored_levels:
            self.report_explorer_achievements_progress(player)

    def _set_level(self, player: PlayerDict) -> None:
        if self.config.level is None:
            return

        if self.config.level < 1 or self.config.level > len(self.required_xp):
            self.error(f'Invalid character level specified: {self.config.level}')
        else:
            self.debug(f' - Updating to level {self.config.level}')
            lower = self.required_xp[self.config.level - 1]
            if self.config.level == len(self.required_xp):
                if player[3][0][1] != lower:
                    player[3][0][1] = lower
                    self.debug(f'   - Also updating XP to {lower}')
            else:
                upper = self.required_xp[self.config.level]
                if player[3][0][1] < lower or player[3][0][1] >= upper:
                    player[3][0][1] = lower
                    self.debug(f'   - Also updating XP to {lower}')
            player[2] = [[0, self.config.level]]

    def _set_money(self, player: PlayerDict) -> None:
        if all(
            x is None
            for x in [
                self.config.money,
                self.config.eridium,
                self.config.moonstone,
                self.config.seraph,
                self.config.torgue,
            ]
        ):
            return

        raw = player[6][0][1]
        b = io.BytesIO(raw)
        values = []
        while b.tell() < len(raw):
            values.append(read_protobuf_value(b, 0))
        if self.config.money is not None:
            self.debug(f' - Setting available money to {self.config.money}')
            values[0] = self.config.money
        if self.config.eridium is not None:
            self.debug(f' - Setting available eridium to {self.config.eridium}')
            values[1] = self.config.eridium
        if self.config.moonstone is not None:
            self.debug(f' - Setting available moonstone to {self.config.moonstone}')
            values[1] = self.config.moonstone
        if self.config.seraph is not None:
            self.debug(f' - Setting available Seraph Crystals to {self.config.seraph}')
            values[2] = self.config.seraph
        if self.config.torgue is not None:
            self.debug(f' - Setting available Torgue Tokens to {self.config.torgue}')
            values[4] = self.config.torgue
        player[6][0] = [0, values]

    def _set_item_level(self, player: PlayerDict) -> None:
        seen_level_1_warning = False
        if self.config.item_levels is not None:
            if self.config.item_levels > 0:
                self.debug(f' - Setting all items to level {self.config.item_levels}')
                level = self.config.item_levels
            else:
                level = player[2][0][1]
                self.debug(f' - Setting all items to character level ({level})')
            for field_number in (53, 54):
                for field in player[field_number]:
                    field_data = read_protobuf(field[1])
                    is_weapon, item, key = self.unwrap_item(field_data[1][0][1])
                    item_4 = item[4]
                    if item_4 is not None:
                        if self.config.force_item_levels or item_4 > 1:
                            item = item[:4] + [level, level] + item[6:]
                            field_data[1][0][1] = self.wrap_item(is_weapon=is_weapon, values=item, key=key)
                            field[1] = write_protobuf(field_data)
                        else:
                            if item_4 == 1 and not seen_level_1_warning:
                                seen_level_1_warning = True
                                self.debug('   NOTICE: At least one item is level 1 and will not be updated.')
                                self.debug('   Use --forceitemlevels to update these items')

    def _set_overpowered_level(self, player: PlayerDict) -> None:
        if self.config.op_level is not None:
            set_op_level = False
            self.debug(f' - Setting OP Level to {self.config.op_level}')

            # Constructing the new value ahead of time since we'll need it
            # no matter what else happens below.
            # This little signed/unsigned dance is awful, but it lets us put the
            # value in as the same format we got it.  So: awesome. Byte order
            # shouldn't actually matter here so long as it's consistent.
            new_field_data = struct.unpack(
                '>Q', struct.pack('>q', -(4 | (max(0, min(self.config.op_level, 0x7FFFFF)) << 8)))
            )[0]

            # Now actually get on with it
            if self.config.op_level > 0:
                if player[7][0][1] < 2 and 'uvhm' not in self.config.unlock:
                    self.config.unlock['uvhm'] = True
                    self.debug('   - Also unlocking UVHM mode')
            for field in player[53]:
                field_data = read_protobuf(field[1])
                if 2 in field_data:
                    is_weapon, item, key = self.unwrap_item(field_data[1][0][1])
                    # TODO: refactor condition below to function
                    if item[0] == 255 and all([val == 0 for val in item[1:]]):
                        idnum = (-field_data[2][0][1]) & 0xFF
                        # An ID of 4 is the one we're after
                        if idnum == 4:
                            field_data[2][0][1] = new_field_data
                            field[1] = write_protobuf(field_data)
                            set_op_level = True
                            break
            if not set_op_level:
                # If we didn't find an existing structure, we'll have to add our
                # own in
                self.debug('   - Creating new OP Level "virtual" item')
                # More magic from Gibbed code
                base_data = (
                    b"\x07\x00\x00\x00\x00\x39\x2a\xff"
                    + b"\x00\x00\x00\x00\x00\x00\x00\x00"
                    + b"\x00\x00\x00\x00\x00\x00\x00\x00"
                    + b"\x00\x00\x00\x00\x00\x00\x00\x00"
                    + b"\x00\x00\x00\x00\x00\x00\x00\x00"
                )
                # noinspection PyDictCreation
                entry = {}
                entry[1] = [[2, base_data]]
                entry[2] = [[0, new_field_data]]
                entry[3] = [[0, 0]]
                entry[4] = [[0, 0]]
                player[53].append([2, write_protobuf(entry)])

    def _set_backpack(self, player: PlayerDict) -> None:
        if self.config.backpack is None:
            return

        self.debug(f' - Setting backpack size to {self.config.backpack}')
        size = self.config.backpack
        sdu_size = int(math.ceil((size - self.min_backpack_size) / 3.0))
        self.debug(f'   - Setting SDU size to {sdu_size}')
        new_size = self.min_backpack_size + (sdu_size * 3)
        if size != new_size:
            self.debug(f'   - Resetting backpack size to {new_size} to match SDU count')
        slots = read_protobuf(player[13][0][1])
        slots[1][0][1] = new_size
        player[13][0][1] = write_protobuf(slots)
        s = read_repeated_protobuf_value(player[36][0][1], 0)
        player[36][0][1] = write_repeated_protobuf_value(s[:7] + [sdu_size] + s[8:], 0)

    def _set_bank(self, player: PlayerDict) -> None:
        if self.config.bank is None:
            return

        self.debug(f' - Setting bank size to {self.config.bank}')
        size = self.config.bank
        sdu_size = int(min(255, math.ceil((size - self.min_bank_size) / 2.0)))
        self.debug(f'   - Setting SDU size to {sdu_size}')
        new_size = self.min_bank_size + (sdu_size * 2)
        if size != new_size:
            self.debug(f'   - Resetting bank size to {new_size} to match SDU count')
        if 56 in player:
            player[56][0][1] = new_size
        else:
            player[56] = [[0, new_size]]
        s = read_repeated_protobuf_value(player[36][0][1], 0)
        if len(s) < 9:
            s = s + (9 - len(s)) * [0]
        player[36][0][1] = write_repeated_protobuf_value(s[:8] + [sdu_size] + s[9:], 0)

    def _set_gun_slots(self, player: PlayerDict) -> None:
        if self.config.gun_slots is None:
            return

        self.debug(f' - Setting available gun slots to {self.config.gun_slots}')
        n = self.config.gun_slots
        slots = read_protobuf(player[13][0][1])
        slots[2][0][1] = n
        if slots[3][0][1] > n - 2:
            slots[3][0][1] = n - 2
        player[13][0][1] = write_protobuf(slots)

    def _copy_nvhm_missions(self, player: PlayerDict) -> None:
        if not self.config.copy_nvhm_missions:
            return

        self.debug(' - Copying NVHM mission status to TVHM+UVHM')
        if 'uvhm' not in self.config.unlock:
            self.config.unlock['uvhm'] = True
            self.debug('   - Also unlocking UVHM mode')
        player[18][1][1] = player[18][0][1]
        player[18][2][1] = player[18][0][1]

    def _unlock_slaughterdome(self, player: PlayerDict) -> None:
        if 'slaughterdome' not in self.config.unlock:
            return

        unlocked, notifications = b'', b''
        if 23 in player:
            unlocked = player[23][0][1]
        if 24 in player:
            notifications = player[24][0][1]
        self.debug(' - Unlocking Creature Slaughterdome')
        if 1 not in unlocked:
            unlocked += b"\x01"
        if 1 not in notifications:
            notifications += b"\x01"
        player[23] = [[2, unlocked]]
        player[24] = [[2, notifications]]

    def _unlock_tvhm_uvhm(self, player: PlayerDict) -> None:
        if 'uvhm' in self.config.unlock:
            self.debug(' - Unlocking UVHM (and TVHM)')
            if player[7][0][1] < 2:
                player[7][0][1] = 2
        elif 'tvhm' in self.config.unlock:
            self.debug(' - Unlocking TVHM')
            if player[7][0][1] < 1:
                player[7][0][1] = 1

    def _unlock_base_challenges(self, player: PlayerDict) -> None:
        if 'challenges' not in self.config.unlock:
            return

        self.debug(' - Unlocking all non-level-specific challenges')
        challenge_unlocks = [apply_structure(read_protobuf(d[1]), self.save_structure[38][2]) for d in player[38]]
        inverted_structure = invert_structure(self.save_structure[38][2])
        seen_challenges = {}
        for unlock in challenge_unlocks:
            seen_challenges[unlock['name'].decode('latin1')] = True
        for challenge in sorted(self.challenges.values()):
            if challenge.id_text in seen_challenges:
                continue
            player[38].append(
                [
                    2,
                    write_protobuf(
                        remove_structure(
                            {
                                'dlc_id': challenge.category.dlc,
                                'is_from_dlc': challenge.category.is_from_dlc,
                                'name': challenge.id_text,
                            },
                            inverted_structure,
                        )
                    ),
                ]
            )

    def _unlock_features(self, player: PlayerDict) -> None:
        if not self.config.unlock:
            return

        self._unlock_slaughterdome(player)
        self._unlock_tvhm_uvhm(player)
        self._unlock_base_challenges(player)

        if 'ammo' in self.config.unlock:
            self.debug(' - Unlocking ammo capacity')
            s = read_repeated_protobuf_value(player[36][0][1], 0)
            for idx2, (key2, _value) in enumerate(zip(self.black_market_keys, s)):
                if key2 in self.black_market_ammo:
                    s[idx2] = 7
            player[36][0][1] = write_repeated_protobuf_value(s, 0)

    def _set_max_ammo(self, player: PlayerDict) -> None:
        if self.config.max_ammo is None:
            return

        self.debug(' - Setting ammo pools to maximum')

        # First we got a figure out our black market levels
        s = read_repeated_protobuf_value(player[36][0][1], 0)
        assert len(self.black_market_keys) == len(s)
        bm_levels = dict(zip(self.black_market_keys, s))

        # Make a dict of what our max ammo is for each of our black market
        # ammo pools
        max_ammo = {}
        for ammo_type, ammo_level in bm_levels.items():
            if ammo_type not in self.black_market_ammo:
                continue

            ammo_values = self.black_market_ammo[ammo_type]
            if len(ammo_values) - 1 < ammo_level:
                max_ammo[ammo_type] = (len(ammo_values) - 1, ammo_values[-1])
            else:
                max_ammo[ammo_type] = (ammo_level, ammo_values[ammo_level])

        # Now loop through our 'resources' structure and modify to
        # suit, updating 'amount' and 'level' as we go.
        inverted_structure = invert_structure(self.save_structure[11][2])
        seen_ammo = {}
        for idx, protobuf in enumerate(player[11]):
            data2 = apply_structure(read_protobuf(protobuf[1]), self.save_structure[11][2])
            resource = data2['resource'].decode('latin1')
            if resource in self.ammo_resource_lookup:
                ammo_type = self.ammo_resource_lookup[resource]
                seen_ammo[ammo_type] = True
                if ammo_type in max_ammo:
                    # Set the data in the structure
                    data2['level'] = max_ammo[ammo_type][0]
                    data2['amount'] = float(max_ammo[ammo_type][1])

                    # And now convert back into a protobuf
                    player[11][idx][1] = write_protobuf(remove_structure(data2, inverted_structure))

                else:
                    self.error(f'Ammo type "{ammo_type}" / pool "{data2["pool"]}" not found!')
            else:
                self.error(f'Ammo pool "{resource}" not found!')

        # Also, early in the game there isn't an entry in here for, for instance,
        # rocket launchers.  So let's make sure that all our known ammo exists.
        for ammo_type in bm_levels.keys():
            if ammo_type in self.ammo_resources.keys() and ammo_type not in seen_ammo:
                new_struct = {
                    'resource': self.ammo_resources[ammo_type][0],
                    'pool': self.ammo_resources[ammo_type][1],
                    'level': max_ammo[ammo_type][0],
                    'amount': float(max_ammo[ammo_type][1]),
                }
                player[11].append([2, write_protobuf(remove_structure(new_struct, inverted_structure))])

    def _handle_challenges(self, player: PlayerDict) -> None:
        if not self.config.challenges:
            return

        data2 = self.unwrap_challenges(player[15][0][1])
        # You can specify multiple options at once.  Specifying "max" and
        # "bonus" at the same time, for instance, will put everything at its
        # max value, and then potentially lower the ones which have bonuses.
        do_zero = 'zero' in self.config.challenges
        do_max = 'max' in self.config.challenges
        do_bonus = 'bonus' in self.config.challenges

        self.debug(' - Working with challenge data:')
        if do_zero:
            self.debug('   - Setting challenges to 0')
        if do_max:
            self.debug('   - Setting challenges to max-1')
        if do_bonus:
            self.debug('   - Setting bonus challenges')

        for save_challenge in data2['challenges']:
            if save_challenge['id'] not in self.challenges:
                continue

            if do_zero:
                save_challenge['total_value'] = save_challenge['previous_value']
            if do_max:
                save_challenge['total_value'] = (
                    save_challenge['previous_value'] + self.challenges[save_challenge['id']].get_max()
                )
            if do_bonus and self.challenges[save_challenge['id']].bonus:
                bonus_value = save_challenge['previous_value'] + self.challenges[save_challenge['id']].get_bonus()
                if do_max or do_zero or save_challenge['total_value'] < bonus_value:
                    save_challenge['total_value'] = bonus_value

        player[15][0][1] = self.wrap_challenges(data2)

    def _fix_challenge_overflow(self, player: PlayerDict) -> None:
        # TODO: rewrite as standalone function and move to bl2_routines.py
        if not self.config.fix_challenge_overflow:
            return

        self.notice('Fix challenge overflow')
        data2 = self.unwrap_challenges(player[15][0][1])

        for save_challenge in data2['challenges']:
            if save_challenge['id'] in self.challenges:
                if save_challenge['total_value'] >= 2000000000:
                    self.notice(f'fix overflow in: {save_challenge["_name"]}')
                    save_challenge['total_value'] = self.challenges[save_challenge['id']].get_max() + 1

        player[15][0][1] = self.wrap_challenges(data2)

    def _set_character_name(self, player: PlayerDict) -> None:
        if self.config.name is None:
            return

        self.debug(f' - Setting character name to {self.config.name!r}')
        data2 = apply_structure(read_protobuf(player[19][0][1]), self.save_structure[19][2])
        data2['name'] = self.config.name
        player[19][0][1] = write_protobuf(remove_structure(data2, invert_structure(self.save_structure[19][2])))

    def _set_save_game_id(self, player: PlayerDict) -> None:
        if self.config.save_game_id is None:
            return

        self.debug(f' - Setting save slot ID to {self.config.save_game_id}')
        player[20][0][1] = self.config.save_game_id

    def modify_save(self, data: bytes) -> bytes:
        """
        Performs a set of modifications on file data, based on our
        config object.  "data" should be the raw data from a save
        file.

        Note that if a user is both showing info and making changes,
        we're parsing the protobuf twice, since show_save_info also does
        that.  Inefficiency!
        """

        player = read_protobuf(self.unwrap_player_data(data))

        self._set_level(player)
        self._set_money(player)

        # Note that this block should always come *after* the block which sets
        # character level, in case we've been instructed to set items to the
        # character's level.
        self._set_item_level(player)

        # OP Level is stored in a weird little custom item.
        # See Gibbed.Borderlands2.FileFormats/SaveExpansion.cs for a bit more
        # rigorous example of how to process those properly.
        # Note that this needs to happen before the unlock section, since
        # it may trigger an unlock of UVHM if that wasn't already specified.
        self._set_overpowered_level(player)

        self._set_backpack(player)
        self._set_bank(player)
        self._set_gun_slots(player)
        self._copy_nvhm_missions(player)
        self._unlock_features(player)

        # This should always come after the ammo-unlock section, since our
        # max ammo will change if more black market SDUs are unlocked.
        self._set_max_ammo(player)

        self._handle_challenges(player)
        self._fix_challenge_overflow(player)
        self._set_character_name(player)
        self._set_save_game_id(player)

        self._reset_challenge_or_mission(player)

        return self.wrap_player_data(write_protobuf(player))

    def export_items(self, data, output) -> None:
        """
        Exports items stored in savegame data 'data' to the open
        filehandle 'output'
        """
        player = read_protobuf(self.unwrap_player_data(data))
        skipped_count = 0
        for i, name in ((41, "Bank"), (53, "Items"), (54, "Weapons")):
            count = 0
            content = player.get(i)
            if content is None:
                continue
            print(f'; {name}', file=output)
            for field in content:
                raw: bytes = read_protobuf(field[1])[1][0][1]

                # Borderlands uses some sort-of "fake" items to store some DLC
                # data.  As per the Gibbed sourcecode, this includes:
                #   1. "Currency On Hand"  (?)
                #   2. Last Playthrough Number / Playthroughs completed
                #   3. "Has played in UVHM"
                #   4. Overpower levels unlocked
                #   5. Last Overpower selection
                #
                # The data for these is stored in the `unknown2` field, by this
                # app's data definitions (or the protobuf's [2] index).  Regardless,
                # these aren't actual items, so we're skipping them.  See Gibbed's
                # Gibbed.Borderlands2.FileFormats/SaveExpansion.cs for details
                # on how to parse the `unknown2` field.
                is_weapon, item, key = self.unwrap_item(raw)
                if item[0] == 255 and all([val == 0 for val in item[1:]]):
                    skipped_count += 1
                else:
                    count += 1
                    raw_bytes = replace_raw_item_key(raw, 0)
                    printable = base64.b64encode(raw_bytes).decode("latin1")
                    code = f'{self.item_prefix}({printable})'
                    print(code, file=output)
            self.debug(f' - {name} exported: {count}')
        # Don't bother reporting on skipped items, actually, since I now
        # know what they're actually used for.
        # self.debug(f' - Empty items skipped: {skipped_count}')

    def get_fully_explored_areas(self, player: PlayerDict) -> list[str]:
        """
        Reuse converting full player data to json
        for simpler code
        """
        json_data = apply_structure(player, self.save_structure)
        if 'explored_areas' not in json_data:
            return []
        names = [x.decode('utf-8') for x in json_data['explored_areas']]
        return names

    def report_explorer_achievements_progress(self, player: PlayerDict) -> None:
        self.notice(f'No explorer achievements info in {self.__class__.__name__}')

    def create_save_structure(self) -> Dict[int, Any]:
        raise NotImplementedError()

    @staticmethod
    def setup_game_specific_args(parser: argparse.ArgumentParser) -> None:
        """Function to add game-specific arguments."""
        pass

    @staticmethod
    def notice(message) -> None:
        print(message)

    @staticmethod
    def error(message: str) -> None:
        print(f'ERROR: {message}', file=sys.stderr)

    def debug(self, message: str) -> None:
        if self.config.verbose:
            self.notice(message)

    def _read_input_file(self) -> Union[str, bytes]:
        if self.config.input_filename == '-':
            self.debug('Using STDIN for input file')
            return sys.stdin.read()
        else:
            self.debug(f'Opening {self.config.input_filename} for input file')
            with open(self.config.input_filename, 'rb') as inp:
                return inp.read()

    def _convert_json(self, save_data: Union[str, bytes]) -> Union[str, bytes]:
        if not self.config.json:
            return save_data

        self.debug('Interpreting JSON data')
        data = json.loads(save_data)
        if '1' not in data:
            # This means the file had been output as 'json'
            data = remove_structure(data, invert_structure(self.save_structure))
        return self.wrap_player_data(write_protobuf(data))

    def _import_items(self, save_data: bytes) -> Union[str, bytes]:
        """
        Imports items into savegame data "data" based on the passed-in
        item list in "codelist"
        """
        if not self.config.import_items:
            return save_data

        self.debug(f'Importing items from {self.config.import_items}')
        with open(self.config.import_items) as inp:
            raw_items_data = inp.read()

        player = read_protobuf(self.unwrap_player_data(save_data))

        prefix_length = len(self.item_prefix) + 1

        bank_count = 0
        weapon_count = 0
        item_count = 0

        to_bank = False
        for line in raw_items_data.splitlines():
            line = line.strip()
            if line.startswith(";"):
                name = line[1:].strip().lower()
                if name == "bank":
                    to_bank = True
                elif name in ("items", "weapons"):
                    to_bank = False
                continue
            elif not (line.startswith(self.item_prefix + '(') and line.endswith(')')):
                continue

            code = line[prefix_length:-1]
            try:
                code_bytes = base64.b64decode(code)
            except binascii.Error:
                continue

            key = random.randrange(0x100000000) - 0x80000000
            code_bytes = replace_raw_item_key(code_bytes, key)
            if to_bank:
                bank_count += 1
                field = 41
                entry = {1: [[2, code_bytes]]}
            elif (code_bytes[0] & 0x80) == 0:
                item_count += 1
                field = 53
                entry = {1: [[2, code_bytes]], 2: [[0, 1]], 3: [[0, 0]], 4: [[0, 1]]}
            else:
                weapon_count += 1
                field = 54
                entry = {1: [[2, code_bytes]], 2: [[0, 0]], 3: [[0, 1]]}

            player.setdefault(field, []).append([2, write_protobuf(entry)])

        self.debug(f' - Bank imported: {bank_count}')
        self.debug(f' - Items imported: {item_count}')
        self.debug(f' - Weapons imported: {weapon_count}')

        return self.wrap_player_data(write_protobuf(player))

    def _prepare_output_file(self) -> Optional[Tuple[IO, bool]]:
        self.debug('')
        outfile = self.config.output_filename

        if outfile == '-':
            self.debug('Using STDOUT for output file')
            return sys.stdout, False

        self.debug(f'Use {outfile!r} for output file')
        if os.path.isdir(outfile):
            raise BorderlandsError(f'Output file is an existing directory: {outfile!r}')
        elif os.path.isfile(outfile):
            if self.config.force:
                self.debug(f'Overwriting output file {outfile!r}')
                os.unlink(outfile)
            else:
                # TODO: what is the point of checking input file name?
                if self.config.input_filename == '-':
                    raise BorderlandsError(
                        f'Output filename {outfile!r}' + ' exists and --force not specified, aborting'
                    )
                else:
                    self.notice('')
                    self.notice(f'Output filename {outfile!r} exists')
                    sys.stdout.flush()
                    sys.stderr.flush()
                    sys.stderr.write('Continue and overwrite? [y|N] ')
                    sys.stderr.flush()
                    answer = sys.stdin.readline()
                    if answer[0].lower() == 'y':
                        os.unlink(outfile)
                    else:
                        self.notice('')
                        self.notice('Abort.')
                        return None
        if self.config.output in ('savegame', 'decoded'):
            mode = 'wb'
        else:
            mode = 'w'

        output_file = open(outfile, mode)
        return output_file, True

    def _reset_challenge_or_mission(self, player: PlayerDict) -> None:
        pass

    def run(self):
        """
        Main routine - loads data, does things to it, and then writes
        out a file.
        """

        self.debug('')
        save_data = self._read_input_file()

        # If we're reading from JSON, convert it
        save_data = self._convert_json(save_data)

        # If we've been told to import items, do so.
        save_data = self._import_items(save_data)

        # Now perform any changes
        self.debug('Performing requested changes')
        new_data = self.modify_save(save_data)

        self.show_save_info(new_data)

        # If we have an output file, write to it!
        if self.config.output_filename is None:
            if new_data != save_data:
                sys.exit('Changes were made but no output file specified')

            self.debug('No output file specified. Exiting!')
            return

        # Open output file
        output_file_info = self._prepare_output_file()
        if output_file_info is None:
            return
        output_file, close = output_file_info

        # Now output based on what we've been told to do
        if self.config.output == 'items':
            self.debug('Exporting items')
            self.export_items(new_data, output_file)
        elif self.config.output == 'savegame':
            self.debug('Writing savegame file')
            output_file.write(new_data)
        else:
            player = self.unwrap_player_data(new_data)
            if self.config.output in ('decodedjson', 'json'):
                self.debug('Converting to JSON for more human-readable output')
                data = read_protobuf(player)
                if self.config.output == 'json':
                    data = apply_structure(data, self.save_structure)
                player = json.dumps(conv_binary_to_str(data), sort_keys=True, indent=4)
            output_file.write(player)

        if close:
            output_file.close()

        self.notice('Done.')

    @staticmethod
    def setup_currency_args(parser) -> None:
        raise NotImplementedError()
