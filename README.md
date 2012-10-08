# Read and write Borderlands 2 save files

A simple command line utility to extract player information from a Borderlands
2 save file, or to create a new save file from player information.

Note the following before trying to use it:

* It has no graphical interface and is not easy to use
* It does not provide any mechanisms for creating or modifying items and weapons
* It is a proof of concept and will corrupt your save files if used improperly
* It requires a working Python 2 interpreter (2.6 or later) and the Python LZO
  bindings.

## How do I modify values in a save file?

Modify save file data by changing one or more of "level", "skillpoints",
"money", or "eridium":

    ./savefile.py -m eridium=99 < old.sav > new.sav

Or many changes at once, separated by commas:

    ./savefile.py -m level=1,skillpoints=42,money=1234,eridium=9 < old.sav > new.sav

Add --little-endian to write the save file in a way that should be readable by
the PC version (the default is to write the data in big-endian format, for the
console versions):

    ./savefile.py -m eridium=99 --little-endian < old.sav > new.sav

## How do I convert a PC save to work on a console?

A PC save file is automatically detected and read, and the default is to write
in the correct format for a console so this will happen by default.  If you
don't want to make any changes except in the format:

    ./savefile.py -m "" < pc.sav > console.sav

## How do I convert a console save to work on a PC?

As mentioned earlier, add --little-endian to the command to write the data in a
format suitable for the PC.  If you don't want to make any changes except in
the format:

    ./savefile.py -m "" --little-endian < console.sav > pc.sav

## How do I just extract the player data?

Extract the raw protobuf data from a save file:

    ./savefile.py -d < your-save-game.sav > player.p

Extract the data in JSON format (encoded to allow round-tripping):

    ./savefile.py -d -j < your-save-game.sav > player.json

Extract the data in JSON format, applying further protobuf decoding to the
listed fields to show information such as money and eridium:

    ./savefile.py -d -j -p 6:0,8,11,13,18,19,29,30,34,38,53,54 < your-save-game.sav > player.json

## How do I write the player data back to a new save file?

Create a new save file from protobuf data:

    ./savefile.py < player.p > your-new-save-game.sav

Create a new save file from the JSON data:

    ./savefile.py -j < player.json > your-new-save-game.sav
