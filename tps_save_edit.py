#!/usr/bin/env python3
import sys

from borderlands.base_save_edit import run

if __name__ == '__main__':
    run(game_name='TPS', args=sys.argv[1:])
