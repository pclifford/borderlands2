# Borderlands 2 / Borderlands: The Pre-Sequel Save File Modification Tool

This is a simple command line utility to extract and modify player information
from a Borderlands 2 or Borderlands: The Pre-Sequel save file.  It offers a
simple way to perform common actions on a character, such as setting money,
unlocking Black Market SDUs, and can also generate a hand-editable JSON file
which can then be converted back into a savegame.

Note the following before trying to use it:

* It has no graphical interface and is not easy to use
* It does not provide any mechanisms for creating items or weapons, or even
  editing items/weapons in a useful fashion.
* It is a proof of concept and can corrupt your save files **(take backups!)**
* It requires a working Python 3 interpreter (if you need the old Python 2
  version, change to the `python2` branch).  As of March 5, 2022, the minimum
  Python version is 3.9.

This repository is a fork of the original at https://github.com/pclifford/borderlands2

There are several difference between this fork and the original.  The most
obvious difference is in the method of specifying modification arguments.
Also, the original version defaulted to writing savegames usable on consoles,
whereas this fork defaults to writing savegames usable on PC.  The `-b` or
`--bigendian` argument can be specified to have this fork generate
Console-appropriate files, though note that many of the changes since the fork
have not been tested on consoles.  If there are problems with console
integration, contact me and I'd be happy to try and fix it.

Note too that the JSON generated by this fork isn't going to be compatible
with the JSON generated by the main branch, so don't try to mix between the
two.

# Running the program

There are two executables: `bl2_save_edit.py` and `tps_save_edit.py`, for
Borderlands 2 and Borderlands: The Pre-Sequel, respectively.  The functionality
of both is virtually identical, only differing in a few of the modification
options (`--moonstone` instead of `--eridium`, for instance).

The basic form of the utility is to specify and input and output file.  If no
other options are given, the utility effectively just copies the savegame
without making any changes, like so:

    python bl2_save_edit.py save0001.sav save0002.sav

# Input and Output

By default, the utility saves in a format usable by Borderlands, but you can
specify alternate outputs to use, using the `-o` or `--output` option.  The
most useful outputs are:

* **`savegame`** - This is the default, and the only output usable by Borderlands itself.
* **`json`** - This is the most human-editable format, saved in a text-based
  heirarchy in JSON format, which should be fairly reasonable to work with.
* **`items`** - This will save the character's inventory and bank into a text
  file which can then be imported into other tools like Gibbed, or imported
  into other characters using this tool.

For example, saving to a JSON file for later hand-editing:

    python bl2_save_edit.py -o json save0001.sav testing.json

After hand-editing a JSON file, you can convert it back by specifying the `-j`
or `--json` option, to tell the utility that you're loading from a JSON file,
like so:

    python bl2_save_edit.py -j testing.json save0002.sav
    python bl2_save_edit.py --json testing.json save0002.sav

To save the character's inventory to a text file:

    python bl2_save_edit.py --output items save0001.save items.txt

To later import the items in `items.txt` to a savegame, use the `-i` or
`--import-items` argument:

    python bl2_save_edit.py -i items.txt save0002.sav new.sav
    python bl2_save_edit.py --import-items items.txt save0002.sav new.sav

*(note that the savefile with the imported items is `new.sav` - You'd have
to copy that back over to `save0002.sav` afterwards)*

## Other Output Formats

There are also a couple other output formats you can specify with `-o`, though
they are primarily only useful to programmers looking to work with the raw data
a little more closely:

* **`decoded`** - The raw protocol buffer data, after decompression.
* **`decodedjson`** - A midway point between `decoded` and `json`, this will generate
  a JSON file, so it'll be technically editable by hand, but most of the internal
  data structures will be present as raw protobuf strings.

# Modifying Savegames (JSON Method)

As mentioned above, one way to edit your characters is to save them out
as a parsed JSON file, edit the JSON by hand (in a text editor), and then
re-export the JSON into a savefile.  As always, make sure to take backups
of your savefiles before overwriting them.

1. `python bl2_save_edit.py -o json save0001.sav to_edit.json`
2. Edit `to_edit.json` in a text editor, to suit
3. `python bl2_save_edit.py -j to_edit.json save0001.sav`

# Modifying Savegames (Using Commandline Arguments)

Alternatively, you can alter many attributes of your character by just using
commandline options.  You can specify as few or as many of these as you want.
Note that if you specify `-o items` to save a character's items to a text
file, the majority of these options will have no effect.

## Character Name

This can be done with the `--name` option:

    python bl2_save_edit.py --name "Gregor Samsa" old.sav new.sav

## Save Game ID

This is probably not actually useful; Borderlands seems to automatically set
this to a value it thinks is appropriate.  The ID tends to match the filename,
though, and I personally end up setting it just because it seems to make sense
to.  You'll probably be fine if you never touch this option.  It can be
changed with `--save-game-id` like so:

    python bl2_save_edit.py --save-game-id 2 save0001.sav save0002.sav

## Character Level

This will also update your character's XP if needed, and is available with the
`--level` option:

    python bl2_save_edit.py --level 72 old.sav new.sav

## Money

Set money with the `--money` option:

    python bl2_save_edit.py --money 3000000 old.sav new.sav

## Eridium (Borderlands 2 Only)

Set available Eridium with the `--eridium` option.  Note that the game will
reduce this to a maxmimum of 500 if you attempt to add more:

    python bl2_save_edit.py --eridium 500 old.sav new.sav

## Moonstone (Borderlands: The Pre-Sequel Only)

Set available Moonstone with the `--moonstone` option.  Note that the game will
reduce this to a maxmimum of 500 if you attempt to add more:

    python tps_save_edit.py --moonstone 500 old.sav new.sav

## Seraph Crystals (Borderlands 2 Only)

Set the available Seraph Crystals with the `--seraph` option.  The game will
enforce a maximum of 999:

    python bl2_save_edit.py --seraph 999 old.sav new.sav

## Torgue Tokens (Borderlands 2 Only)

Set the available Torgue Tokens with the `--torgue` option.  The game will
enforce a maximum of 999:

    python bl2_save_edit.py --torgue 999 old.sav new.sav

## Item Levels

The `--itemlevels` argument can be used to set all items in your inventory to
either your character's current level, or to the level you specify.

To set to the character's level:

    python bl2_save_edit.py --itemlevels 0 old.sav new.sav

To set to a specific level:

    python bl2_save_edit.py --itemlevels 50 old.sav new.sav

Note that items of level 1, however, are left alone unless you also specify
the `--forceitemlevels` flag:

    python bl2_save_edit.py --itemlevels 0 --forceitemlevels old.sav new.sav

## Backpack Size

The `--backpack` option can be used to set the size of your backpack.  To set
the maximum possible size of the backpack, either specify 39 or "max". Note
that the utility will also enforce that the backpack size is a multiple of 3,
and between the range of 12 and 39.

    python bl2_save_edit.py --backpack max old.sav new.sav
    python bl2_save_edit.py --backpack 31 old.sav new.sav

## Bank Size

Similarly, the `--bank` option can be used to set the size of your bank, and
will round up to multiples of 2, between 6 and 24.  To specify the maximum
value, either use 24 or "max".

    python bl2_save_edit.py --bank max old.sav new.sav
    python bl2_save_edit.py --bank 16 old.sav new.sav

## Gun Slots

The `--gunslots` option can be used to set the total number of open gun slots
(ordinarily unlocked via story missions).  Valid values are 2, 3, and 4:

    python bl2_save_edit.py --gunslots 2 old.sav new.sav
    python bl2_save_edit.py --gunslots 3 old.sav new.sav
    python bl2_save_edit.py --gunslots 4 old.sav new.sav

## Unlocks

There are a few things which can be unlocked via this utility, with the `--unlock`
option.  This option can be specified more than once to unlock more than one
thing.

### Ammo

This option will unlock all ammo SDU upgrades (ordinarily available in the black
market).  This will also automatically refill all ammo pools:

    python bl2_save_edit.py --unlock ammo old.sav new.sav

### Challenges

Some challenges do not actually appear in the challenge list until certain
prerequisites are met.  For instance, the challenge for long-range shotgun
kills doesn't actually appear until the challenge for short-range shotgun
kills has reached level 5.  This will unlock all those challenges regardless
of the prerequisites.  *(Note: this only applies to non-level-specific
challenges)*

    python bl2_save_edit.py --unlock challenges old.sav new.sav

### True Vault Hunter Mode (playthrough 2)

To unlock TVHM:

    python bl2_save_edit.py --unlock tvhm old.sav new.sav

### Ultimate Vault Hunter Mode (playthrough 3)

To unlock UVHM (and also TVHM):

    python bl2_save_edit.py --unlock uvhm old.sav new.sav

### Creature Slaughterdome (Borderlands 2 Only)

**NOTE:** I'm unsure whether or not this would actually work on a system
without the Creature Slaughterdome explicitly enabled, but it's possible maybe
it does?

The Creature Slaughterdome might be unlockable with:

    python bl2_save_edit.py --unlock slaughterdome old.sav new.sav

## Overpower Levels (Borderlands 2 Only)

To set OP Levels:

    python bl2_save_edit.py --oplevel 8 old.sav new.sav

This will also trigger an unlock of TVHM/UVHM if the save does not already
have UVHM unlocked.

## Ammo

The `--maxammo` option can be used to refill all ammo to its current maximum
level (based on what you've already purchased at the black market).  This
is obviously a bit silly ordinarily, given how easy ammo is to come by.

    python bl2_save_edit.py --maxammo old.sav new.sav

To actually increase your total available ammo pool, as you'd do through the
black market, use `--unlock ammo` *(see above)*.  Doing so will then also refill
ammo as if `--maxammo` had been specified.

## Challenge Levels

This option is admittedly rather silly, but the `--challenges` argument will
let you set your character's challenge levels to the specified values.  The
valid options are:

* zero
* max
* bonus

If set to `zero`, the level of all your non-level-specific challenges will be
reset to zero, so you can start accumulating again.  (Possibly useful if you
want to start from scratch but haven't completed enough to use the in-game
reset.)

    python bl2_save_edit.py --challenges zero old.sav new.sav

If set to `max`, the level of all non-level-specific challenges will be set to
*one under* than their maximum level, possibly making it easier to accrue a
good deal of Badass Rank very quickly.

    python bl2_save_edit.py --challenges max old.sav new.sav

If set to `bonus`, the level of all non-level-specific challenges will be set
to *one under* the levels at which they provide bonus skins/heads, for the
challenges which do so.  It will leave all other challenges alone.

    python bl2_save_edit.py --challenges bonus old.sav new.sav

It's also possible to specify both `max` and `bonus`, in which case all
challenges will be set just under their completion level, except for the ones
which provide bonuses, which will then be set to be primed to receive those
bonuses:

    python bl2_save_edit.py --challenges max --challenges bonus old.sav new.sav

## Copying mission data from NVHM to TVHM+UVHM

This is a very specific thing which I can't imagine anyone but me would ever
be looking for, but it's in here anyway because I needed it once.  Basically,
whatever the mission state is from NVHM will be copied to the other two
playthroughs, so they'll appear to be at the exact same state.  This will
also unlock TVHM/UVHM if need be.

    python bl2_save_edit.py --copy-nvhm-missions old.sav new.sav

# Combining Commandline Options

In general, the various options can be combined.  To make a few changes to a
savegame but save as parsed JSON:

    python bl2_save_edit.py --name "Laura Palmer" --save-game-id 2 --money 3000000 --output json save0001.sav laura.json

To take that JSON, unlock TVHM and Challenges, and set challenges to their
primed "bonus" levels, and save as a real savefile:

    python bl2_save_edit.py --json --unlock tvhm --unlock challenges --challenges bonus laura.json save0002.sav

# Working with Savegames to/from Consoles

**NOTE:** As mentioned above, this fork has not actually been tested on
Consoles, so it's possible that the generated savegames might not work.  Use
at your own risk!

The safest way to convert a PC savegame to Console, or vice-versa, would be to
use JSON as an intermediate step.  For the commands which deal with the
console savegames, be sure to specify the `-b` or `--bigendian` options.  For
instance, to convert from a Console savegame to a PC savegame:

    python savegame.py -b -o json xbox.sav pc.json
    python savegame.py -j pc.json pc.sav

Or to convert from a PC savegame to a Console savegame:

    python savegame.py --output json pc.sav xbox.json
    python savegame.py --json --bigendian xbox.json xbox.sav

# Exporting character items

All items stored and held in the character's bank or inventory can be exported
to a text file as a list of codes, in a format compatible with Gibbed's save
editor.  This is accomplished with `-o items` or `--output items` like so:

    python bl2_save_edit.py -o items savegame.sav items.txt

# Importing character items

A text file of codes generated as above, or assembled by hand, can be imported
into a character using the `-i` or `--import-items` arguments, like so:

    python bl2_save_edit.py -i items.txt old.sav new.sav
    python bl2_save_edit.py --import-items items.txt old.sav new.sav

By default all items will be inserted into the inventory, but this can be
changed with a line containing "; Bank" to indicate that all following items
should go into the bank, or one of either "; Weapons" or "; Items" to indicate
that all following items should go into the inventory.  For example, importing
a file containing the following will put a Vault Hunter's Relic into the
inventory and a Righteous Infinity pistol into the bank:

    ; Bank
    BL2(h0Hd1Z+jY/s2Qy++Zu8Ba9qXoOmjwJ6NhrlsOmhNMX+oJo5CfQns)
    ; Items
    BL2(B2vuv4tz1zSQCf2pqLJCS5XD/tKN4FXpjRJLnn1v85U=)

# Other commandline options

There are a few other commandline options available when running the utilities.

## Quiet Output

By default, the utility is rather chatty and will tell you what it's doing
at all times.  To disable output except for errors, use the `-q` or `--quiet`
option:

    python bl2_save_edit.py -q old.sav new.sav
    python bl2_save_edit.py --quiet old.sav new.sav

## Force Overwrites

By default, the utility will refuse to overwrite a file without getting
confirmation from the user first.  To disable that yes/no prompt and force
the app to overwrite the file automatically, use `-f` or `--force` like so:

    python bl2_save_edit.py -f old.sav new.sav
    python bl2_save_edit.py --force old.sav new.sav

## Help

The utility will also show you what all of its commandline options are
at the commandline, using the `-h` or `--help` options:

    python bl2_save_edit.py -h
    python bl2_save_edit.py --help

Sample output from that option is shown below, though might get out-of-date
if I forget to update this README after updating the program:

```
usage: tps_save_edit.py [-h] [-o {savegame,decoded,decodedjson,json,items}]
                          [-i IMPORT_ITEMS] [-j] [-b] [-q] [-f] [--name NAME]
                          [--save-game-id SAVE_GAME_ID] [--level LEVEL]
                          [--money MONEY] [--moonstone MOONSTONE]
                          [--itemlevels ITEMLEVELS] [--forceitemlevels]
                          [--backpack BACKPACK] [--bank BANK]
                          [--gunslots {2,3,4}]
                          [--unlock {tvhm,uvhm,challenges,ammo}]
                          [--challenges {zero,max,bonus}] [--maxammo]
                          input_filename output_filename

Modify Borderlands: The Pre-Sequel Save Files

positional arguments:
  input_filename        Input filename, can be "-" to specify STDIN
  output_filename       Output filename, can be "-" to specify STDOUT

optional arguments:
  -h, --help            show this help message and exit
  -o {savegame,decoded,decodedjson,json,items}, --output {savegame,decoded,decodedjson,json,items}
                        Output file format. The most useful to humans are:
                        savegame, json, and items (default: savegame)
  -i IMPORT_ITEMS, --import-items IMPORT_ITEMS
                        read in codes for items and add them to the bank and
                        inventory (default: None)
  -j, --json            read savegame data from JSON format, rather than
                        savegame (default: False)
  -b, --bigendian       change the output format to big-endian, to write
                        PS/xbox save files (default: False)
  -q, --quiet           quiet output (should generate no output unless there
                        are errors) (default: True)
  -f, --force           force output file overwrite, if the destination file
                        exists (default: False)
  --name NAME           Set the name of the character (default: None)
  --save-game-id SAVE_GAME_ID
                        Set the save game slot ID of the character (probably
                        not actually needed ever) (default: None)
  --level LEVEL         Set the character to this level (from 1 to 72)
                        (default: None)
  --money MONEY         Money to set for character (default: None)
  --moonstone MOONSTONE
                        Moonstone to set for character (default: None)
  --itemlevels ITEMLEVELS
                        Set item levels (to set to current player level,
                        specify 0).Skips level 1 items unless
                        --forceitemlevels is specified too (default: None)
  --forceitemlevels     Set item levels even if the item is at level 1
                        (default: False)
  --backpack BACKPACK   Set size of backpack (maximum is 39, "max" may be
                        specified) (default: None)
  --bank BANK           Set size of bank(maximum is 24, "max" may be
                        specified) (default: None)
  --gunslots {2,3,4}    Set number of gun slots open (default: None)
  --unlock {tvhm,uvhm,challenges,ammo}
                        Game features to unlock (default: {})
  --challenges {zero,max,bonus}
                        Levels to set on challenge data (default: {})
  --maxammo             Fill all ammo pools to their maximum (default: False)
```

# TODO

1. Borderlands:TPS has a bunch more data stored in the file that we don't
   currently parse, so the JSON generated with `-o json` includes a pretty
   large `_raw` section up at the top, for all the data we don't know about.
   The Gibbed editor seems to know about some of these, and I'd sort of like to
   go through and see if anything's worth decoding for this utility.

2. The internal `modify_save` function starts off with the raw, decoded
   protobuf, and each little snippet in there decodes further as-needed, and
   then re-encodes once it's done.  I wonder if it'd make more sense to just
   unwrap the whole thing to JSON at the beginning and then re-wrap at the end,
   rather than doing it piecemeal like that.  The current method is sort of
   nice in that only the bits of the file that actually *need* to get touched
   are processed, but on the other hand, it adds a bunch of unnecessary cruft
   in there.

