from typing import Dict, Callable

PlayerDict = Dict[int, list]
PlayerPatchProc = Callable[[PlayerDict, str], None]
