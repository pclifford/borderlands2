from typing import Final, Dict, Optional, Set

from borderlands.challenges import unwrap_challenges, wrap_challenges
from borderlands.datautil.data_types import PlayerDict, PlayerPatchProc
from borderlands.datautil.protobuf import read_protobuf, write_protobuf

_BL2_MODE_NAMES: Final = {0: 'Normal Mode', 1: 'TVHM', 2: 'UVHM'}


def _is_doctor_orders_mission(mission_data: list) -> bool:
    if len(mission_data) < 2:
        return False
    item1 = mission_data[1]
    if not isinstance(item1, bytes):
        return False
    return b'GD_Z2_DoctorsOrders.M_DoctorsOrders' in item1


def _reset_doctors_orders(player: PlayerDict, _endian: str) -> None:
    """
    - remove mission entry with name
        "GD_Z2_DoctorsOrders.M_DoctorsOrders"
    - do it in order: UVHM -> TVHM -> Normal
    - exit after first successful reset
    """
    player18 = player[18]
    len18 = len(player18)
    for mode_index in range(len18 - 1, -1, -1):
        vh_mode_data = player18[mode_index]

        unpacked = read_protobuf(vh_mode_data[1])
        if 3 not in unpacked:
            continue
        raw_missions = unpacked[3]
        fixed_missions = [x for x in raw_missions if not _is_doctor_orders_mission(x)]
        unpacked[3] = fixed_missions

        vh_mode_data[1] = write_protobuf(unpacked)

        player18[mode_index] = vh_mode_data

        if len(raw_missions) != len(fixed_missions):
            print('  reset Doctor\'s Orders for', _BL2_MODE_NAMES.get(mode_index, 'Unknown'))
            break

    player[18] = player18


def _reset_bad_touch(player: PlayerDict, endian: str) -> None:
    """
    Bad Touch SMG flag is one per player for all the Normal/TVHM/UVHM

    It could be easily spoiled by teammate so here is the fix
    """
    data2 = unwrap_challenges(data=player[15][0][1], challenges={}, endian=endian)

    for save_challenge in data2['challenges']:
        if save_challenge['id'] == 1836:
            print('1836:', repr(save_challenge))
            save_challenge['total_value'] = 0

    player[15][0][1] = wrap_challenges(data=data2, endian=endian)


_RESET_OPT_DATA: Final[Dict[str, PlayerPatchProc]] = {
    'bad-touch': _reset_bad_touch,
    'doctors-orders': _reset_doctors_orders,
}


def get_reset_proc(key: str) -> Optional[PlayerPatchProc]:
    return _RESET_OPT_DATA.get(key)


def get_valid_reset_option_values() -> Set[str]:
    return set(_RESET_OPT_DATA.keys())
