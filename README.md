A simple command line utility to extract player information from a Borderlands
2 save file, or to create a new save file from player information.

Note the following before trying to use it:

* It has no graphical interface and is not easy to use
* It does not provide any mechanisms for creating or modifying items and weapons
* It is a proof of concept and will corrupt your save files if used improperly
* It requires a working Python 2 interpreter (2.6 or later) and the Python LZO
  bindings.

Examples:

Extract the raw protobuf data from a save file:

    ./savefile.py -d < your-save-game.sav > player.p

Create a new save file from protobuf data:

    ./savefile.py < player.p > your-new-save-game.sav

Extract the data in JSON format (encoded to allow round-tripping):

    ./savefile.py -d -j < your-save-game.sav > player.json

Extract the data in JSON format, applying further protobuf decoding to the
listed fields:

    ./savefile.py -d -j -p 6:0,8,11,13,18,19,29,30,34,38,53,54 < your-save-game.sav > player.json

Create a new save file from the JSON data:

    ./savefile.py -j < player.json > your-new-save-game.sav

Modify save file data by changing one or more of "level", "skillpoints",
"money", or "eridium":

    ./savefile.py -m eridium=99 < old.sav > new.sav

Or many changes at once, separated by commas:

    ./savefile.py -m level=1,skillpoints=42,money=1234,eridium=9 < old.sav > new.sav
