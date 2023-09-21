#!/usr/bin/env python3

import sys
import traceback
from typing import List

from borderlands.bl2 import AppBL2
from borderlands.bltps import AppTPS
from borderlands.savefile import BaseApp

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

    # noinspection PyBroadException
    try:
        app: BaseApp
        if game_name == 'BL2':
            app = AppBL2(args)
        elif game_name == 'TPS':
            app = AppTPS(args)
        else:
            raise RuntimeError(f'unknown game: {game_name!r}')

        app.run()

    except Exception:
        sys.stdout.flush()
        sys.stderr.flush()
        print(ERROR_TEMPLATE.format(repr(args)), file=sys.stderr)
        traceback.print_exc(None, sys.stderr)
        sys.exit(1)
