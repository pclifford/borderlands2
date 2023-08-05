from typing import Tuple, Optional


class ChallengeCategory:
    """
    Simple little class to hold information about challenge
    categories.  Mostly just a glorified dict.
    """

    def __init__(self, name: str, dlc: int = 0) -> None:
        self.name = name
        self.dlc = dlc
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


def create_bl2_challenge_that_is_accepted(
    *,
    position: int,
    identifier: int,
    id_text: str,
    category: ChallengeCategory,
    name: str,
    description: str,
    levels: Tuple[int, ...],
    bonus: Optional[int] = None,
) -> Challenge:
    return Challenge(
        position=position,
        identifier=identifier,
        id_text=id_text,
        category=category,
        name=name,
        description=description,
        levels=levels,
        bonus=bonus,
        bl2_is_in_challenge_accepted=True,
    )
