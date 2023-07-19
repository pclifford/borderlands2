import argparse
import os
from typing import Union, Optional, List, Callable


def adjust_value(*, prev: Optional[Union[str, int]], min_value: int, max_value: int, label: str) -> Optional[int]:
    if prev is None:
        return None

    assert min_value <= max_value

    if prev == 'max':
        return max_value

    try:
        int_value = int(prev)
    except ValueError:
        raise argparse.ArgumentTypeError(f'{label} value {prev!r} is not a number')

    if int_value > max_value:
        return max_value
    if int_value < min_value:
        return min_value
    return int_value


class Config(argparse.Namespace):
    """
    Class to hold our configuration information.  Note that
    we're NOT using a separate class for BL2 and BLTPS configs,
    since so much of it is the same.
    """

    # Given by the user, booleans
    json = False
    big_endian = False
    verbose = True
    force = False
    copy_nvhm_missions = False
    print_unexplored_levels = False

    # Given by the user, strings
    import_items = None
    output = 'savegame'
    input_filename = '-'
    output_filename = '-'

    # Former 'modify' options
    name = None
    save_game_id = None
    level = None
    money = None
    eridium = None
    moonstone = None
    seraph = None
    torgue = None
    item_levels = None
    backpack = None
    bank = None
    gun_slots = None
    max_ammo = None
    op_level = None
    unlock = {}
    challenges = {}
    fix_challenge_overflow = False

    # Config options interpreted from the above
    endian = '<'
    changes = False
    show_info = False

    def finish(
        self,
        *,
        parser: argparse.ArgumentParser,
        max_level: int,
        min_backpack_size: int,
        max_backpack_size: int,
        min_bank_size: int,
        max_bank_size: int,
    ) -> None:
        """
        Some extra sanity checks on our options.  "parser" should
        be an active ArgumentParser object we can use to raise
        errors.  "app" is an App object which we use for a couple
        lookups.
        """

        # byte order
        if self.big_endian:
            self.endian = '>'
        else:
            self.endian = '<'

        # If we're unlocking ammo, also set maxammo
        if 'ammo' in self.unlock:
            self.max_ammo = True

        # Set our "changes" boolean -- first, args which take a value
        if any(
            x is not None
            for x in [
                self.backpack,
                self.bank,
                self.eridium,
                self.fix_challenge_overflow,
                self.gun_slots,
                self.item_levels,
                self.level,
                self.max_ammo,
                self.money,
                self.moonstone,
                self.name,
                self.op_level,
                self.save_game_id,
                self.seraph,
                self.torgue,
            ]
        ):
            self.changes = True

        # Next, boolean args which are set to True
        if self.copy_nvhm_missions:
            self.changes = True

        # Finally, any unlocks/challenges we mean to set
        if any(bool(var) for var in [self.unlock, self.challenges]):
            self.changes = True

        # Now set our "show_info" boolean.  Just a single boolean option, at the moment
        if self.print_unexplored_levels:
            self.show_info = True

        # Can't read/write to the same file
        if (
            self.output_filename is not None
            and self.input_filename != '-'
            and os.path.abspath(self.input_filename) == os.path.abspath(self.output_filename)
        ):
            parser.error('input_filename and output_filename cannot be the same file')

        # If the user specified --level, make sure it's from 1 to 80
        if self.level is not None:
            if self.level < 1:
                parser.error('level must be at least 1')
            if self.level > max_level:
                parser.error(f'level can be at most {max_level}')

        self.backpack = adjust_value(
            prev=self.backpack,
            min_value=min_backpack_size,
            max_value=max_backpack_size,
            label='Backpack',
        )

        self.bank = adjust_value(prev=self.bank, min_value=min_bank_size, max_value=max_bank_size, label='Bank')


class DictAction(argparse.Action):
    """
    Custom argparse action to put list-like arguments into
    a dict (where the value will be True) rather than a list.
    This is probably implemented fairly shoddily.
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """
        Constructor, taken right from https://docs.python.org/2.7/library/argparse.html#action
        """
        if nargs is not None:
            raise ValueError('nargs is not allowed')
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Actually setting a value.  Forces the attr into a dict if it isn't already.
        """
        arg_value = getattr(namespace, self.dest)
        if not isinstance(arg_value, dict):
            arg_value = {}
        arg_value[values] = True
        setattr(namespace, self.dest, arg_value)


def parse_args(
    *,
    args: List[str],
    setup_currency_args: Callable[[argparse.ArgumentParser], None],
    setup_game_specific_args: Callable[[argparse.ArgumentParser], None],
    game_name: str,
    max_level: int,
    min_backpack_size: int,
    max_backpack_size: int,
    min_bank_size: int,
    max_bank_size: int,
    unlock_choices: List[str],
):
    """
    Parse our arguments.
    """

    def non_empty_string(s):
        if len(s) > 0:
            return s
        raise argparse.ArgumentTypeError("Value must have length greater than 0")

    def positive_int(value):
        try:
            result = int(value)
        except Exception:
            raise argparse.ArgumentTypeError(f'positive integer value required: {value!r}')

        if result > 0:
            return result

        raise argparse.ArgumentTypeError(f'positive integer value required: {result!r}')

    # Set up our config object
    config = Config()

    parser = argparse.ArgumentParser(
        description=f'Modify {game_name} Save Files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Optional args

    parser.add_argument(
        '-o',
        '--output',
        choices=['savegame', 'decoded', 'decodedjson', 'json', 'items', 'none'],
        default='savegame',
        help="""
                Output file format.  The most useful to humans are: savegame, json, and items.
                If no output file is specified, this will revert to `none`.
                """,
    )

    parser.add_argument(
        '-i',
        '--import-items',
        dest='import_items',
        help='read in codes for items and add them to the bank and inventory',
    )

    parser.add_argument(
        '-j',
        '--json',
        action='store_true',
        help='read savegame data from JSON format, rather than savegame',
    )

    parser.add_argument(
        '-b',
        '--bigendian',
        action='store_true',
        dest='big_endian',
        help='change the output format to big-endian, to write PS/xbox save files',
    )

    parser.add_argument(
        '-q',
        '--quiet',
        dest='verbose',
        action='store_false',
        help='quiet output (should generate no output unless there are errors)',
    )

    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='force output file overwrite, if the destination file exists',
    )

    # More optional args - used to be the "modify" option

    parser.add_argument(
        '--name',
        type=non_empty_string,
        help='Set the name of the character',
    )

    parser.add_argument(
        '--save-game-id',
        dest='save_game_id',
        type=positive_int,
        help='Set the save game slot ID of the character (probably not actually needed ever)',
    )

    parser.add_argument(
        '--level',
        type=int,
        help=f'Set the character to this level (from 1 to {max_level})',
    )

    parser.add_argument(
        '--money',
        type=int,
        help='Money to set for character',
    )

    # B2 and TPS have different currency types, so this function is
    # implemented in the implementing classes.
    setup_currency_args(parser)

    parser.add_argument(
        '--itemlevels',
        type=int,
        dest='item_levels',
        help='Set item levels (to set to current player level, specify 0).'
        'Skips level 1 items unless --forceitemlevels is specified too',
    )

    parser.add_argument(
        '--forceitemlevels',
        action='store_true',
        dest='force_item_levels',
        help='Set item levels even if the item is at level 1',
    )

    parser.add_argument(
        '--backpack',
        help=f'Set size of backpack (maximum is {max_backpack_size}, "max" may be specified)',
    )

    parser.add_argument(
        '--bank',
        help=f'Set size of bank (maximum is {max_bank_size}, "max" may be specified)',
    )

    parser.add_argument(
        '--gunslots',
        type=int,
        choices=[2, 3, 4],
        dest='gun_slots',
        help='Set number of gun slots open',
    )

    parser.add_argument(
        '--copy-nvhm-missions',
        dest='copy_nvhm_missions',
        action='store_true',
        help='Copies NVHM mission state to both TVHM and UVHM modes.  Also unlocks TVHM/UVHM',
    )

    parser.add_argument(
        '--unlock',
        action=DictAction,
        choices=unlock_choices,
        default={},
        help='Game features to unlock',
    )

    parser.add_argument(
        '--challenges',
        action=DictAction,
        choices=['zero', 'max', 'bonus'],
        default={},
        help='Levels to set on challenge data',
    )

    parser.add_argument(
        '--maxammo',
        action='store_true',
        dest='max_ammo',
        help='Fill all ammo pools to their maximum',
    )

    parser.add_argument(
        '--fix-challenge-overflow',
        action='store_true',
        help='Fix values for challenges which appear as huge negative numbers',
    )

    parser.add_argument(
        '--print-unexplored-levels',
        action='store_true',
        help='Print level names that are not fully explored by player',
    )

    # Positional args

    parser.add_argument('input_filename', help='Input filename, can be "-" to specify STDIN')

    parser.add_argument(
        'output_filename',
        nargs='?',
        help="""
                Output filename, can be "-" to specify STDOUT.  Can be optional, in
                which case no output file is produced.
                """,
    )

    # Additional game-specific arguments
    setup_game_specific_args(parser)

    # Actually parse the args
    parser.parse_args(args, config)

    # Do some extra fiddling
    config.finish(
        parser=parser,
        max_level=max_level,
        min_backpack_size=min_backpack_size,
        max_backpack_size=max_backpack_size,
        min_bank_size=min_bank_size,
        max_bank_size=max_bank_size,
    )

    # Some sanity checking with output type and output_filename
    if config.output_filename is None:
        # If we requested any changes, the only sensible course is to write them out
        if config.changes:
            parser.error("No output_filename was specified, but changes were requested")

        # If we manually specified an output type, we'll also need an output filename.
        # It's possible in this case that the user explicitly set `savegame` as the
        # output, rather than just leaving it at the default, but I don't think it's
        # worth the shenanigans necessary to detect that.
        if config.output not in {'savegame', 'none'}:
            parser.error(f"No output_filename was specified, but output type '{config.output}' was specified")

        # If we got here, we're probably good, but force ourselve to `none` output
        config.output = 'none'

    else:
        # If we have an output filename but `none` output, complain about it.
        if config.output == 'none':
            parser.error("Output filename specified but with `none` output")

    return config
