# Read and write Borderlands 2 save files

A simple command line utility to extract player information from a Borderlands
2 save file, or to create a new save file from player information.

Note the following before trying to use it:

* It has no graphical interface and is not easy to use
* It does not provide any mechanisms for creating items or weapons
* It is a proof of concept and will corrupt your save files if used improperly
* It requires a working Python 2 interpreter (2.6 or later, not 3)

## How do I modify values in a save file?

Modify save file data by changing one or more of "level", "skillpoints",
"money", "eridium", or "itemlevels":

    python savefile.py -m eridium=99 old.sav new.sav

Set the levels of all your items and weapons to match your character's level:

    python savefile.py -m itemlevels old.sav new.sav

Or to a specific level:

    python savefile.py -m itemlevels=20 old.sav new.sav

Or many changes at once, separated by commas:

    python savefile.py -m level=7,skillpoints=42,money=1234,eridium=9,itemlevels old.sav new.sav

Add --little-endian to write the save file in a format that should be readable
by the PC version (the default is to write the data in big-endian format, for
the console versions):

    python savefile.py -m eridium=99 --little-endian old.sav new.sav

## How do I convert a PC save to work on a console?

A PC save file is automatically detected and read, and the default is to write
in the correct format for a console.  If you don't want to make any changes
except to the format:

    python savefile.py -m "" pc.sav console.sav

## How do I convert a console save to work on a PC?

As before, add --little-endian to the command to write the data in a format
suitable for the PC.  If you don't want to make any changes except to the
format:

    python savefile.py -m "" --little-endian console.sav pc.sav

## How do I just extract the player data?

Extract the raw protocol buffer data from a save file:

    python savefile.py -d your-save-game.sav player.p

Extract the data in JSON format (encoded to allow round-tripping):

    python savefile.py -d -j your-save-game.sav player.json

Extract the data in JSON format, applying further protocol buffer decoding to
the listed fields to show information such as money and eridium:

    python savefile.py -d -j -p 6:0,8,11,13,18,19,29,30,34,38,53,54 your-save-game.sav player.json

## How do I write the player data back to a new save file?

Create a new save file from protocol buffer data:

    python savefile.py player.p your-new-save-game.sav

Create a new save file from the JSON data:

    python savefile.py -j player.json your-new-save-game.sav

As before, to write a save file that can be read by the PC version add the
--little-endian flag to one of the above, eg:

    python savefile.py -j --little-endian player.json your-new-save-game.sav
