#!/usr/bin/env python3

import sys
import traceback
from typing import List

from borderlands.bl2 import AppBL2
from borderlands.bltps import AppTPS

MIN_PYTHON = (3, 9)

ERROR_TEMPLATE = """
Something went wrong, but please ensure you have the latest
version from https://github.com/apocalyptech/borderlands2 before
reporting a bug.  Information useful for a report follows:

Arguments: {}

"""


def python_version_check():
    if sys.version_info < MIN_PYTHON:
        sys.exit(
            f'ERROR: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} is required to run this utility'
            + f' but you use {sys.version_info[0]}.{sys.version_info[1]}'
        )


def run(*, game_name: str, args: List[str]) -> None:
    python_version_check()

    if game_name == 'BL2':
        app_class = AppBL2
    elif game_name == 'TPS':
        app_class = AppTPS
    else:
        raise RuntimeError(f'unknown game: {game_name!r}')

    # noinspection PyBroadException
    try:
        app = app_class(args)
        app.run()
    except Exception:
        print(ERROR_TEMPLATE.format(repr(args)), file=sys.stderr)
        traceback.print_exc(None, sys.stderr)
        sys.exit(1)
