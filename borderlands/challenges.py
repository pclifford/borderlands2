import io
import struct
from typing import Tuple, Optional, Dict

from borderlands.datautil.errors import BorderlandsError


class ChallengeCategory:
    """
    Simple little class to hold information about challenge
    categories.  Mostly just a glorified dict.
    """

    def __init__(self, name: str, dlc: int = 0, bl2_is_in_challenge_accepted: bool = False) -> None:
        self.name = name
        self.dlc = dlc
        self.bl2_is_in_challenge_accepted = bl2_is_in_challenge_accepted
        if self.dlc == 0:
            self.is_from_dlc = 0
        else:
            self.is_from_dlc = 1


class Challenge:
    """
    A simple little object to hold information about our non-level-specific
    challenges.  This is *mostly* just a glorified dict.
    """

    def __init__(
        self,
        *,
        position: int,
        identifier: int,
        id_text: str,
        category: ChallengeCategory,
        name: str,
        description: str,
        levels: Tuple[int, ...],
        bonus: Optional[int] = None,
        bl2_is_in_challenge_accepted: bool = False,
    ) -> None:
        self.position = position
        self.identifier = identifier
        self.id_text = id_text
        self.category = category
        self.name = name
        self.description = description
        self.levels = levels
        self.bonus = bonus
        self.bl2_is_in_challenge_accepted = bl2_is_in_challenge_accepted

    def get_max(self) -> int:
        """
        Returns the point value for the challenge JUST before its maximum level.
        """
        return self.levels[-1] - 1

    def get_bonus(self) -> Optional[int]:
        """
        Returns the point value for the challenge JUST before getting the challenge's
        bonus reward, if any.  Will return None if no bonus is present for the
        challenge.
        """
        if self.bonus is None:
            return None
        else:
            return self.levels[self.bonus - 1] - 1

    def __lt__(self, other) -> bool:
        return self.id_text.lower() < other.id_text.lower()


def unwrap_challenges(*, data: bytes, challenges: Dict[int, Challenge], endian: str) -> dict:
    """
    Unwraps our challenge data.  The first ten bytes are a header:

        int32: Unknown, is always "4" on my savegames, though.
        int32: Size in bytes of all the challenges, plus two more bytes
               for the next short
        short: Number of challenges

    Each challenge takes up a total of 12 bytes, so num_challenges*12
    should always equal size_in_bytes-2.

    The structure of each challenge is:

        byte: unknown, possibly at least part of an ID, but not unique
              on its own
        byte: unknown, but is always (on my saves, anyway) 6 or 7.
        byte: unknown, but is always 1.
        int32: total value of the challenge, across all resets
        byte: unknown, but is always 1
        int32: previous, pre-challenge-reset value.  Will always be 0
               until challenges have been reset at least once.

    The first two bytes of each challenge can be taken together, and if so, can
    serve as a unique identifier for the challenge.  I decided to read them in
    that way, as a short value.  I wasn't able to glean any pattern to whether
    a 6 or a 7 shows up in the second byte.

    Once your challenges have been reset in-game, the previous value is copied
    into that second int32, but the total value itself remains unchanged, so at
    that point you need to subtract previous_value from total_value to find the
    actual current state of the challenge (that procedure is obviously true
    prior to any resets, too, since previous_value is just zero in that case).

    It's also worth mentioning that challenge data keeps accumulating even
    after the challenge itself is completed, so the number displayed in-game
    for completed challenges is no longer accurate.

    """

    unknown, size_in_bytes, num_challenges = struct.unpack(endian + 'IIH', data[:10])
    # Sanity check on size reported
    if (size_in_bytes + 8) != len(data):
        raise BorderlandsError(f'Challenge data reported as {size_in_bytes} bytes, but {len(data) - 8} bytes found')

    # Sanity check on number of challenges reported
    if (num_challenges * 12) != (size_in_bytes - 2):
        raise BorderlandsError(f'{num_challenges} challenges reported, but {size_in_bytes - 2} bytes of data found')

    # Now read them in
    challenges_result = []
    for challenge in range(num_challenges):
        idx = 10 + (challenge * 12)
        challenge_dict = dict(
            zip(
                ['id', 'first_one', 'total_value', 'second_one', 'previous_value'],
                struct.unpack(endian + 'HBIBI', data[idx : idx + 12]),
            )
        )
        challenges_result.append(challenge_dict)

        if challenge_dict['id'] in challenges:
            info = challenges[challenge_dict['id']]
            challenge_dict['_id_text'] = info.id_text
            challenge_dict['_category'] = info.category.name
            challenge_dict['_name'] = info.name
            challenge_dict['_description'] = info.description

    return {'unknown': unknown, 'challenges': challenges_result}


def wrap_challenges(*, data: dict, endian: str) -> bytes:
    """
    Re-wrap our challenge data.  See the notes above in unwrap_challenges for
    details on the structure.

    Note that we are trusting that the correct number of challenges are present
    in our data structure and setting size_in_bytes and num_challenges to match.
    Change the number of challenges at your own risk!
    """

    b = io.BytesIO()
    b.write(
        struct.pack(
            endian + 'IIH',
            data['unknown'],
            (len(data['challenges']) * 12) + 2,
            len(data['challenges']),
        )
    )
    save_challenges = data['challenges']
    for challenge in save_challenges:
        b.write(
            struct.pack(
                endian + 'HBIBI',
                challenge['id'],
                challenge['first_one'],
                challenge['total_value'],
                challenge['second_one'],
                challenge['previous_value'],
            )
        )
    return b.getvalue()
