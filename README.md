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
"money", "eridium", "seraph", "gunslots", "backpack", "bank", "unlocks", or
"itemlevels":

    python savefile.py -m eridium=99 old.sav new.sav

Set the levels of all your items and weapons to match your character's level:

    python savefile.py -m itemlevels old.sav new.sav

Or to a specific level:

    python savefile.py -m itemlevels=20 old.sav new.sav

Set the number of guns your character can have equipped to 2, 3, or 4:

    python savefile.py -m gunslots=4 old.sav new.sav

Set the size of your character's backpack, and the corresponding number of
purchased backpack SDUs:

    python savefile.py -m backpack=27 old.sav new.sav

Set the size of your character's bank, and the corresponding number of
purchased bank SDUs:

    python savefile.py -m bank=16 old.sav new.sav

Unlock the Creature Slaughter Dome (Natural Selection Annex):

    python savefile.py -m unlocks=slaughterdome old.sav new.sav

Unlock the True Vault Hunter mode:

    python savefile.py -m unlocks=truevaulthunter old.sav new.sav

Unlock both at once:

    python savefile.py -m unlocks=slaughterdome:truevaulthunter old.sav new.sav

Or many changes at once, separated by commas:

    python savefile.py -m level=7,skillpoints=42,money=1234,eridium=12,seraph=120,itemlevels old.sav new.sav

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

## How do I take a copy of all my character's items?

All items stored and held in the character's bank or inventory can be exported
to a text file as a list of codes, in a format compatible with Gibbed's save
editor:

    python savefile.py -e items.txt your-save-game.sav

## How do I import those items back into a character?

A text file of codes generated as above, or assembled by hand, can be imported
into a character like so:

    python savefile.py -i items.txt old.sav new.sav

(Don't forget to add --little-endian if you're creating a save file for the PC
version.)

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

## How do I just extract the player data?

Extract the raw protocol buffer data from a save file:

    python savefile.py -d your-save-game.sav player.p

Extract the data in JSON format (encoded purely to preserve all the raw
information -- not very readable):

    python savefile.py -d -j your-save-game.sav player.json

Extract the data in JSON format, applying further parsing to make the data as
readable as possible:

    python savefile.py -d -j -p your-save-game.sav player.json

It may help to copy and paste the contents of the .json file into a site like
http://www.jsoneditoronline.org/ in order to view or modify the contents, to
ensure that the necessary JSON formatting is preserved.

Note that if you modify any of the data you extract in this way there is a very
high probability that you will corrupt your save file.  Please make sure you
have a backup first.

## How do I write the player data back to a new save file?

Create a new save file from protocol buffer data:

    python savefile.py player.p your-new-save-game.sav

Create a new save file from the JSON data:

    python savefile.py -j player.json your-new-save-game.sav

As before, to write a save file that can be read by the PC version add the
--little-endian flag to one of the above, eg:

    python savefile.py -j --little-endian player.json your-new-save-game.sav
