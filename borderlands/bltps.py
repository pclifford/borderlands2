from typing import Any, Dict, List

from borderlands import bltps_data
from borderlands.datautil.common import unwrap_float, wrap_float, unwrap_bytes, wrap_bytes
from borderlands.savefile import BaseApp


class AppTPS(BaseApp):
    """
    Our main application class for Borderlands: The Pre-Sequel
    """

    def __init__(self, args: List[str]) -> None:
        super().__init__(
            args=args,
            item_struct_version=10,
            game_name='Borderlands: The Pre-Sequel',
            item_prefix='BLOZ',
            max_level=70,
            black_market_keys=(
                'rifle',
                'pistol',
                'launcher',
                'shotgun',
                'smg',
                'sniper',
                'grenade',
                'backpack',
                'bank',
                'laser',
            ),
            black_market_ammo={
                'grenade': [3, 4, 5, 6, 7, 8, 9, 10],
                'laser': [500, 620, 740, 860, 980, 1100, 1220, 1340],
                'launcher': [12, 15, 18, 21, 24, 27, 30, 33],
                'pistol': [200, 300, 400, 500, 600, 700, 800, 900],
                'rifle': [280, 420, 560, 700, 840, 980, 1120, 1260],
                'shotgun': [80, 100, 120, 140, 160, 180, 200, 220],
                'smg': [360, 540, 720, 900, 1080, 1260, 1440, 1620],
                'sniper': [48, 60, 72, 84, 96, 108, 120, 132],
            },
            unlock_choices=['tvhm', 'uvhm', 'challenges', 'ammo'],
            challenges=bltps_data.create_bltps_challenges(),
        )

    @staticmethod
    def setup_currency_args(parser) -> None:
        """
        Adds the options we're using to control currency
        """

        parser.add_argument(
            '--moonstone',
            type=int,
            help='Moonstone to set for character',
        )

    def create_save_structure(self) -> Dict[int, Any]:
        """
        Sets up our main save_structure var which controls how we read the file
        """
        return {
            1: "class",
            2: "level",
            3: "experience",
            4: "skill_points",
            6: ("currency", True, 0),
            7: "playthroughs_completed",
            8: ("skills", True, {1: "name", 2: "level", 3: "unknown3", 4: "unknown4"}),
            11: (
                "resources",
                True,
                {1: "resource", 2: "pool", 3: ("amount", False, (unwrap_float, wrap_float)), 4: "level"},
            ),
            13: ("sizes", False, {1: "inventory", 2: "weapon_slots", 3: "weapon_slots_shown"}),
            15: ("stats", False, (self.unwrap_challenges, self.wrap_challenges)),
            16: ("active_fast_travel", True, None),
            17: "last_fast_travel",
            18: (
                "missions",
                True,
                {
                    1: "playthrough",
                    2: "active",
                    3: (
                        "data",
                        True,
                        {
                            1: "name",
                            2: "status",
                            3: "is_from_dlc",
                            4: "dlc_id",
                            5: ("unknown5", False, (unwrap_bytes, wrap_bytes)),
                            6: "unknown6",
                            7: ("unknown7", False, (unwrap_bytes, wrap_bytes)),
                            8: "unknown8",
                            9: "unknown9",
                            10: "unknown10",
                            11: "level",
                        },
                    ),
                },
            ),
            19: (
                "appearance",
                False,
                {
                    1: "name",
                    2: ("color1", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
                    3: ("color2", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
                    4: ("color3", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
                },
            ),
            20: "save_game_id",
            21: "mission_number",
            23: ("unlocks", False, (unwrap_bytes, wrap_bytes)),
            24: ("unlock_notifications", False, (unwrap_bytes, wrap_bytes)),
            25: "time_played",
            26: "save_timestamp",
            29: (
                "game_stages",
                True,
                {
                    1: "name",
                    2: "level",
                    3: "is_from_dlc",
                    4: "dlc_id",
                    5: "playthrough",
                },
            ),
            30: ("areas", True, {1: "name", 2: "unknown2"}),
            34: (
                "id",
                False,
                {
                    1: ("a", False, 5),
                    2: ("b", False, 5),
                    3: ("c", False, 5),
                    4: ("d", False, 5),
                },
            ),
            35: ("wearing", True, None),
            36: ("black_market", False, (self.unwrap_black_market, self.wrap_black_market)),
            37: "active_mission",
            38: ("challenges", True, {1: "name", 2: "is_from_dlc", 3: "dlc_id"}),
            41: (
                "bank",
                True,
                {
                    1: ("data", False, (self.unwrap_item_info, self.wrap_item_info)),
                },
            ),
            43: ("lockouts", True, {1: "name", 2: "time", 3: "is_from_dlc", 4: "dlc_id"}),
            46: ("explored_areas", True, None),
            49: "active_playthrough",
            53: (
                "items",
                True,
                {
                    1: ("data", False, (self.unwrap_item_info, self.wrap_item_info)),
                    2: "unknown2",
                    3: "is_equipped",
                    4: "star",
                },
            ),
            54: (
                "weapons",
                True,
                {
                    1: ("data", False, (self.unwrap_item_info, self.wrap_item_info)),
                    2: "slot",
                    3: "star",
                },
            ),
            55: "stats_bonuses_disabled",
            56: "bank_size",
        }
