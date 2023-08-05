from typing import Dict

from borderlands.challenges import Challenge, ChallengeCategory, create_bl2_challenge_that_is_accepted


def create_bl2_challenges() -> Dict[int, Challenge]:
    # Challenge categories
    challenge_cat_dlc4 = ChallengeCategory("Hammerlock's Hunt", 4)
    challenge_cat_dlc3 = ChallengeCategory("Campaign of Carnage", 3)
    challenge_cat_dlc9 = ChallengeCategory("Dragon Keep", 9)
    challenge_cat_dlc1 = ChallengeCategory("Pirate's Booty", 1)
    challenge_cat_enemies = ChallengeCategory("Enemies")
    challenge_cat_elemental = ChallengeCategory("Elemental")
    challenge_cat_loot = ChallengeCategory("Loot")
    challenge_cat_money = ChallengeCategory("Money and Trading")
    challenge_cat_vehicle = ChallengeCategory("Vehicle")
    challenge_cat_health = ChallengeCategory("Health and Recovery")
    challenge_cat_grenades = ChallengeCategory("Grenades")
    challenge_cat_shields = ChallengeCategory("Shields")
    challenge_cat_rockets = ChallengeCategory("Rocket Launcher")
    challenge_cat_sniper = ChallengeCategory("Sniper Rifle")
    challenge_cat_ar = ChallengeCategory("Assault Rifle")
    challenge_cat_smg = ChallengeCategory("SMG")
    challenge_cat_shotgun = ChallengeCategory("Shotgun")
    challenge_cat_pistol = ChallengeCategory("Pistol")
    challenge_cat_melee = ChallengeCategory("Melee")
    challenge_cat_combat = ChallengeCategory("General Combat")
    challenge_cat_misc = ChallengeCategory("Miscellaneous")

    # There are two possible ways of uniquely identifying challenges in this file:
    # via their numeric position in the list, or by what looks like an internal
    # ID (though that ID is constructed a little weirdly, so I'm not sure if it's
    # actually intended to be used that way or not).
    #
    # I did run some tests, and it looks like internally, B2 probably does use
    # that ID field to identify the challenges...  You can mess around with the
    # order in which they're saved to the file, but so long as the ID field
    # is still pointing to the challenge you want, it'll be read in properly
    # (and then when you save your game, they'll be written back out in the
    # original order).
    #
    # Given that, I decided to go ahead and use that probably-ID field as the
    # index on this dict, rather than the order.  That should be slightly more
    # flexible for anyone editing the JSON directly, and theoretically
    # shouldn't be a problem in the future since there won't be any new major
    # DLC for B2...
    # noinspection PyDictCreation
    challenges: Dict[int, Challenge] = {}

    # Hammerlock DLC Challenges
    challenges[1752] = Challenge(
        position=305,
        identifier=1752,
        id_text="GD_Sage_Challenges.Challenges.Challenge_Sage_KillSavages",
        category=challenge_cat_dlc4,
        name="Savage Bloody Savage",
        description="Kill savages",
        levels=(20, 50, 100, 250, 500),
    )
    challenges[1750] = Challenge(
        position=303,
        identifier=1750,
        id_text="GD_Sage_Challenges.Challenges.Challenge_Sage_KillDrifters",
        category=challenge_cat_dlc4,
        name="Harder They Fall",
        description="Kill drifters",
        levels=(5, 15, 30, 40, 50),
    )
    challenges[1751] = Challenge(
        position=304,
        identifier=1751,
        id_text="GD_Sage_Challenges.Challenges.Challenge_Sage_KillFanBoats",
        category=challenge_cat_dlc4,
        name="Fan Boy",
        description="Kill Fan Boats",
        levels=(5, 10, 15, 20, 30),
    )
    challenges[1753] = Challenge(
        position=306,
        identifier=1753,
        id_text="GD_Sage_Challenges.Challenges.Challenge_Sage_RaidBossA",
        category=challenge_cat_dlc4,
        name="Voracidous the Invincible",
        description="Defeat Voracidous the Invincible",
        levels=(1, 3, 5, 10, 15),
    )
    challenges[1952] = Challenge(
        position=307,
        identifier=1952,
        id_text="GD_Sage_Challenges.Challenges.Challenge_Sage_KillBoroks",
        category=challenge_cat_dlc4,
        name="Boroking Around",
        description="kill boroks",
        levels=(10, 20, 50, 80, 120),
    )
    challenges[1953] = Challenge(
        position=308,
        identifier=1953,
        id_text="GD_Sage_Challenges.Challenges.Challenge_Sage_KillScaylions",
        category=challenge_cat_dlc4,
        name="Stinging Sensation",
        description="Kill scaylions",
        levels=(10, 20, 50, 80, 120),
    )

    # Torgue DLC Challenges
    challenges[1756] = Challenge(
        position=310,
        identifier=1756,
        id_text="GD_Iris_Challenges.Challenges.Challenge_Iris_KillMotorcycles",
        category=challenge_cat_dlc3,
        name="Bikes Destroyed",
        description="Destroy Bikes",
        levels=(10, 20, 30, 50, 80),
    )
    challenges[1757] = Challenge(
        position=311,
        identifier=1757,
        id_text="GD_Iris_Challenges.Challenges.Challenge_Iris_KillBikers",
        category=challenge_cat_dlc3,
        name="Bikers Killed",
        description="Bikers Killed",
        levels=(50, 100, 150, 200, 250),
    )
    challenges[1950] = Challenge(
        position=316,
        identifier=1950,
        id_text="GD_Iris_Challenges.Challenges.Challenge_Iris_TorgueTokens",
        category=challenge_cat_dlc3,
        name="Torgue Tokens Acquired",
        description="Acquire Torgue Tokens",
        levels=(100, 250, 500, 750, 1000),
    )
    challenges[1949] = Challenge(
        position=315,
        identifier=1949,
        id_text="GD_Iris_Challenges.Challenges.Challenge_Iris_BuyTorgueItems",
        category=challenge_cat_dlc3,
        name="Torgue Items Purchased",
        description="Purchase Torgue Items with Tokens",
        levels=(2, 5, 8, 12, 15),
    )
    challenges[1758] = Challenge(
        position=312,
        identifier=1758,
        id_text="GD_Iris_Challenges.Challenges.Challenge_Iris_CompleteBattles",
        category=challenge_cat_dlc3,
        name="Battles Completed",
        description="Complete All Battles",
        levels=(1, 4, 8, 12),
    )
    challenges[1759] = Challenge(
        position=313,
        identifier=1759,
        id_text="GD_Iris_Challenges.Challenges.Challenge_Iris_Raid1",
        category=challenge_cat_dlc3,
        name="Pete The Invincible Defeated",
        description="Defeat Pete the Invincible",
        levels=(1, 3, 5, 10, 15),
    )

    # Tiny Tina DLC Challenges
    challenges[1954] = Challenge(
        position=318,
        identifier=1954,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillDwarves",
        category=challenge_cat_dlc9,
        name="Scot-Free",
        description="Kill dwarves",
        levels=(50, 100, 150, 200, 250),
    )
    challenges[1768] = Challenge(
        position=320,
        identifier=1768,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillGolems",
        category=challenge_cat_dlc9,
        name="Rock Out With Your Rock Out",
        description="Kill golems",
        levels=(10, 25, 50, 80, 120),
    )
    challenges[1769] = Challenge(
        position=321,
        identifier=1769,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillKnights",
        category=challenge_cat_dlc9,
        name="Knighty Knight",
        description="Kill knights",
        levels=(10, 25, 75, 120, 175),
    )
    challenges[1771] = Challenge(
        position=323,
        identifier=1771,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillOrcs",
        category=challenge_cat_dlc9,
        name="Orcs Should Perish",
        description="Kill orcs",
        levels=(50, 100, 150, 200, 250),
    )
    challenges[1772] = Challenge(
        position=324,
        identifier=1772,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillSkeletons",
        category=challenge_cat_dlc9,
        name="Bone Breaker",
        description="Kill skeletons",
        levels=(50, 100, 150, 200, 250),
    )
    challenges[1773] = Challenge(
        position=325,
        identifier=1773,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillSpiders",
        category=challenge_cat_dlc9,
        name="Ew Ew Ew Ew",
        description="Kill spiders",
        levels=(25, 50, 100, 150, 200),
    )
    challenges[1774] = Challenge(
        position=326,
        identifier=1774,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillTreants",
        category=challenge_cat_dlc9,
        name="Cheerful Green Giants",
        description="Kill treants",
        levels=(10, 20, 50, 80, 120),
    )
    challenges[1775] = Challenge(
        position=327,
        identifier=1775,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillWizards",
        category=challenge_cat_dlc9,
        name="Magical Massacre",
        description="Kill wizards",
        levels=(10, 20, 50, 80, 120),
    )
    challenges[1754] = Challenge(
        position=317,
        identifier=1754,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillDragons",
        category=challenge_cat_dlc9,
        name="Fus Roh Die",
        description="Kill dragons",
        levels=(10, 20, 50, 80, 110),
    )
    challenges[1770] = Challenge(
        position=322,
        identifier=1770,
        id_text="GD_Aster_Challenges.Challenges.Challenge_Aster_KillMimics",
        category=challenge_cat_dlc9,
        name="Can't Fool Me",
        description="Kill mimics",
        levels=(5, 15, 30, 50, 75),
    )

    # Captain Scarlett DLC Challenges
    challenges[1743] = Challenge(
        position=298,
        identifier=1743,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_Crystals",
        category=challenge_cat_dlc1,
        name="In The Pink",
        description="Collect Seraph Crystals",
        levels=(80, 160, 240, 320, 400),
    )
    challenges[1755] = Challenge(
        position=299,
        identifier=1755,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_Purchase",
        category=challenge_cat_dlc1,
        name="Shady Dealings",
        description="Purchase Items With Seraph Crystals",
        levels=(1, 3, 5, 10, 15),
    )
    challenges[1745] = Challenge(
        position=294,
        identifier=1745,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_KillWorms",
        category=challenge_cat_dlc1,
        name="Worm Killer",
        description="Kill Sand Worms",
        levels=(10, 20, 30, 50, 80),
    )
    challenges[1746] = Challenge(
        position=295,
        identifier=1746,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_KillBandits",
        category=challenge_cat_dlc1,
        name="Land Lubber",
        description="Kill Pirates",
        levels=(50, 100, 150, 200, 250),
    )
    challenges[1747] = Challenge(
        position=296,
        identifier=1747,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_KillHovercrafts",
        category=challenge_cat_dlc1,
        name="Hovernator",
        description="Destroy Pirate Hovercrafts",
        levels=(5, 10, 15, 20, 30),
    )
    challenges[1748] = Challenge(
        position=297,
        identifier=1748,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_PirateChests",
        category=challenge_cat_dlc1,
        name="Pirate Booty",
        description="Open Pirate Chests",
        levels=(25, 75, 150, 250, 375),
    )
    challenges[1742] = Challenge(
        position=292,
        identifier=1742,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_Raid1",
        category=challenge_cat_dlc1,
        name="Hyperius the Not-So-Invincible",
        description="Divide Hyperius by zero",
        levels=(1, 3, 5, 10, 15),
    )
    challenges[1744] = Challenge(
        position=293,
        identifier=1744,
        id_text="GD_Orchid_Challenges.Challenges.Challenge_Orchid_Raid3",
        category=challenge_cat_dlc1,
        name="Master Worm Food",
        description="Feed Master Gee to his worms",
        levels=(1, 3, 5, 10, 15),
    )

    # Enemies
    challenges[1632] = create_bl2_challenge_that_is_accepted(
        position=24,
        identifier=1632,
        id_text="GD_Challenges.enemies.Enemies_KillSkags",
        category=challenge_cat_enemies,
        name="Skags to Riches",
        description="Kill skags",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1675] = create_bl2_challenge_that_is_accepted(
        position=84,
        identifier=1675,
        id_text="GD_Challenges.enemies.Enemies_KillConstructors",
        category=challenge_cat_enemies,
        name="Constructor Destructor",
        description="Kill constructors",
        levels=(5, 12, 20, 30, 50),
    )
    challenges[1655] = create_bl2_challenge_that_is_accepted(
        position=80,
        identifier=1655,
        id_text="GD_Challenges.enemies.Enemies_KillLoaders",
        category=challenge_cat_enemies,
        name="Load and Lock",
        description="Kill loaders",
        levels=(20, 100, 500, 1000, 1500),
        bonus=3,
    )
    challenges[1651] = create_bl2_challenge_that_is_accepted(
        position=76,
        identifier=1651,
        id_text="GD_Challenges.enemies.Enemies_KillBullymongs",
        category=challenge_cat_enemies,
        name="Bully the Bullies",
        description="Kill bullymongs",
        levels=(25, 50, 150, 300, 750),
    )
    challenges[1652] = create_bl2_challenge_that_is_accepted(
        position=77,
        identifier=1652,
        id_text="GD_Challenges.enemies.Enemies_KillCrystalisks",
        category=challenge_cat_enemies,
        name="Crystals are a Girl's Best Friend",
        description="Kill crystalisks",
        levels=(10, 25, 50, 80, 120),
    )
    challenges[1653] = create_bl2_challenge_that_is_accepted(
        position=78,
        identifier=1653,
        id_text="GD_Challenges.enemies.Enemies_KillGoliaths",
        category=challenge_cat_enemies,
        name="WHY SO MUCH HURT?!",
        description="Kill goliaths",
        levels=(10, 25, 50, 80, 120),
    )
    challenges[1654] = create_bl2_challenge_that_is_accepted(
        position=79,
        identifier=1654,
        id_text="GD_Challenges.enemies.Enemies_KillEngineers",
        category=challenge_cat_enemies,
        name="Paingineering",
        description="Kill Hyperion personnel",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1658] = create_bl2_challenge_that_is_accepted(
        position=83,
        identifier=1658,
        id_text="GD_Challenges.enemies.Enemies_KillSurveyors",
        category=challenge_cat_enemies,
        name="Just a Moment of Your Time...",
        description="Kill surveyors",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1694] = create_bl2_challenge_that_is_accepted(
        position=87,
        identifier=1694,
        id_text="GD_Challenges.enemies.Enemies_KillNomads",
        category=challenge_cat_enemies,
        name="You (No)Mad, Bro?",
        description="Kill nomads",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1695] = create_bl2_challenge_that_is_accepted(
        position=88,
        identifier=1695,
        id_text="GD_Challenges.enemies.Enemies_KillPsychos",
        category=challenge_cat_enemies,
        name="Mama's Boys",
        description="Kill psychos",
        levels=(50, 100, 150, 300, 500),
    )
    challenges[1696] = create_bl2_challenge_that_is_accepted(
        position=89,
        identifier=1696,
        id_text="GD_Challenges.enemies.Enemies_KillRats",
        category=challenge_cat_enemies,
        name="You Dirty Rat",
        description="Kill rats.  Yes, really.",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1791] = create_bl2_challenge_that_is_accepted(
        position=93,
        identifier=1791,
        id_text="GD_Challenges.enemies.Enemies_KillSpiderants",
        category=challenge_cat_enemies,
        name="Pest Control",
        description="Kill spiderants",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1792] = create_bl2_challenge_that_is_accepted(
        position=94,
        identifier=1792,
        id_text="GD_Challenges.enemies.Enemies_KillStalkers",
        category=challenge_cat_enemies,
        name="You're One Ugly Mother...",
        description="Kill stalkers",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1793] = create_bl2_challenge_that_is_accepted(
        position=95,
        identifier=1793,
        id_text="GD_Challenges.enemies.Enemies_KillThreshers",
        category=challenge_cat_enemies,
        name="Tentacle Obsession",
        description="Kill threshers",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1693] = create_bl2_challenge_that_is_accepted(
        position=86,
        identifier=1693,
        id_text="GD_Challenges.enemies.Enemies_KillMarauders",
        category=challenge_cat_enemies,
        name="Marauder? I Hardly Know 'Er!",
        description="Kill marauders",
        levels=(20, 100, 500, 1000, 1500),
        bonus=3,
    )
    challenges[1794] = create_bl2_challenge_that_is_accepted(
        position=96,
        identifier=1794,
        id_text="GD_Challenges.enemies.Enemies_KillVarkid",
        category=challenge_cat_enemies,
        name="Another Bug Hunt",
        description="Kill varkids",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1795] = create_bl2_challenge_that_is_accepted(
        position=97,
        identifier=1795,
        id_text="GD_Challenges.enemies.Enemies_KillGyros",
        category=challenge_cat_enemies,
        name="Die in the Friendly Skies",
        description="Kill buzzards",
        levels=(10, 25, 45, 70, 100),
    )
    challenges[1796] = create_bl2_challenge_that_is_accepted(
        position=98,
        identifier=1796,
        id_text="GD_Challenges.enemies.Enemies_KillMidgets",
        category=challenge_cat_enemies,
        name="Little Person, Big Pain",
        description="Kill midgets",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1895] = create_bl2_challenge_that_is_accepted(
        position=249,
        identifier=1895,
        id_text="GD_Challenges.enemies.Enemies_ShootBullymongProjectiles",
        category=challenge_cat_enemies,
        name="Hurly Burly",
        description="Shoot bullymong-tossed projectiles out of midair",
        levels=(10, 25, 50, 125, 250),
    )
    challenges[1896] = create_bl2_challenge_that_is_accepted(
        position=250,
        identifier=1896,
        id_text="GD_Challenges.enemies.Enemies_ReleaseChainedMidgets",
        category=challenge_cat_enemies,
        name="Short-Chained",
        description="Shoot chains to release midgets from shields",
        levels=(1, 5, 15, 30, 50),
    )
    challenges[1934] = create_bl2_challenge_that_is_accepted(
        position=99,
        identifier=1934,
        id_text="GD_Challenges.enemies.Enemies_KillBruisers",
        category=challenge_cat_enemies,
        name="Cruising for a Bruising",
        description="Kill bruisers",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1732] = create_bl2_challenge_that_is_accepted(
        position=91,
        identifier=1732,
        id_text="GD_Challenges.enemies.Enemies_KillVarkidPods",
        category=challenge_cat_enemies,
        name="Pod Pew Pew",
        description="Kill varkid pods before they hatch",
        levels=(10, 25, 45, 70, 100),
    )

    # Elemental
    challenges[1873] = create_bl2_challenge_that_is_accepted(
        position=225,
        identifier=1873,
        id_text="GD_Challenges.elemental.Elemental_SetEnemiesOnFire",
        category=challenge_cat_elemental,
        name="Cowering Inferno",
        description="Ignite enemies",
        levels=(25, 100, 400, 1000, 2000),
    )
    challenges[1642] = create_bl2_challenge_that_is_accepted(
        position=40,
        identifier=1642,
        id_text="GD_Challenges.elemental.Elemental_KillEnemiesCorrosive",
        category=challenge_cat_elemental,
        name="Acid Trip",
        description="Kill enemies with corrode damage",
        levels=(20, 75, 250, 600, 1000),
    )
    challenges[1645] = create_bl2_challenge_that_is_accepted(
        position=43,
        identifier=1645,
        id_text="GD_Challenges.elemental.Elemental_KillEnemiesExplosive",
        category=challenge_cat_elemental,
        name="Boom.",
        description="Kill enemies with explosive damage",
        levels=(20, 75, 250, 600, 1000),
        bonus=3,
    )
    challenges[1877] = create_bl2_challenge_that_is_accepted(
        position=229,
        identifier=1877,
        id_text="GD_Challenges.elemental.Elemental_DealFireDOTDamage",
        category=challenge_cat_elemental,
        name="I Just Want to Set the World on Fire",
        description="Deal burn damage",
        levels=(2500, 20000, 100000, 500000, 1000000),
        bonus=5,
    )
    challenges[1878] = create_bl2_challenge_that_is_accepted(
        position=230,
        identifier=1878,
        id_text="GD_Challenges.elemental.Elemental_DealCorrosiveDOTDamage",
        category=challenge_cat_elemental,
        name="Corroderate",
        description="Deal corrode damage",
        levels=(2500, 20000, 100000, 500000, 1000000),
    )
    challenges[1879] = create_bl2_challenge_that_is_accepted(
        position=231,
        identifier=1879,
        id_text="GD_Challenges.elemental.Elemental_DealShockDOTDamage",
        category=challenge_cat_elemental,
        name='Say "Watt" Again',
        description="Deal electrocute damage",
        levels=(5000, 20000, 100000, 500000, 1000000),
    )
    challenges[1880] = create_bl2_challenge_that_is_accepted(
        position=232,
        identifier=1880,
        id_text="GD_Challenges.elemental.Elemental_DealBonusSlagDamage",
        category=challenge_cat_elemental,
        name="Slag-Licked",
        description="Deal bonus damage to Slagged enemies",
        levels=(5000, 25000, 150000, 1000000, 5000000),
        bonus=3,
    )

    # Loot
    challenges[1898] = create_bl2_challenge_that_is_accepted(
        position=251,
        identifier=1898,
        id_text="GD_Challenges.Pickups.Inventory_PickupWhiteItems",
        category=challenge_cat_loot,
        name="Another Man's Treasure",
        description="Loot or purchase white items",
        levels=(50, 125, 250, 400, 600),
    )
    challenges[1899] = create_bl2_challenge_that_is_accepted(
        position=252,
        identifier=1899,
        id_text="GD_Challenges.Pickups.Inventory_PickupGreenItems",
        category=challenge_cat_loot,
        name="It's Not Easy Looting Green",
        description="Loot or purchase green items",
        levels=(20, 50, 75, 125, 200),
        bonus=3,
    )
    challenges[1900] = create_bl2_challenge_that_is_accepted(
        position=253,
        identifier=1900,
        id_text="GD_Challenges.Pickups.Inventory_PickupBlueItems",
        category=challenge_cat_loot,
        name="I Like My Treasure Rare",
        description="Loot or purchase blue items",
        levels=(5, 12, 20, 30, 45),
    )
    challenges[1901] = create_bl2_challenge_that_is_accepted(
        position=254,
        identifier=1901,
        id_text="GD_Challenges.Pickups.Inventory_PickupPurpleItems",
        category=challenge_cat_loot,
        name="Purple Reign",
        description="Loot or purchase purple items",
        levels=(2, 4, 7, 12, 20),
    )
    challenges[1902] = create_bl2_challenge_that_is_accepted(
        position=255,
        identifier=1902,
        id_text="GD_Challenges.Pickups.Inventory_PickupOrangeItems",
        category=challenge_cat_loot,
        name="Nothing Rhymes with Orange",
        description="Loot or purchase orange items",
        levels=(1, 3, 6, 10, 15),
        bonus=5,
    )
    challenges[1669] = create_bl2_challenge_that_is_accepted(
        position=108,
        identifier=1669,
        id_text="GD_Challenges.Loot.Loot_OpenChests",
        category=challenge_cat_loot,
        name="The Call of Booty",
        description="Open treasure chests",
        levels=(5, 25, 50, 125, 250),
    )
    challenges[1670] = create_bl2_challenge_that_is_accepted(
        position=109,
        identifier=1670,
        id_text="GD_Challenges.Loot.Loot_OpenLootables",
        category=challenge_cat_loot,
        name="Open Pandora's Boxes",
        description="Open lootable chests, lockers, and other objects",
        levels=(50, 250, 750, 1500, 2500),
        bonus=3,
    )
    challenges[1630] = create_bl2_challenge_that_is_accepted(
        position=8,
        identifier=1630,
        id_text="GD_Challenges.Loot.Loot_PickUpWeapons",
        category=challenge_cat_loot,
        name="Gun Runner",
        description="Pick up or purchase weapons",
        levels=(10, 25, 150, 300, 750),
    )

    # Money
    challenges[1858] = create_bl2_challenge_that_is_accepted(
        position=118,
        identifier=1858,
        id_text="GD_Challenges.Economy.Economy_MoneySaved",
        category=challenge_cat_money,
        name="For the Hoard!",
        description="Save a lot of money",
        levels=(10000, 50000, 250000, 1000000, 3000000),
        bonus=3,
    )
    challenges[1859] = create_bl2_challenge_that_is_accepted(
        position=119,
        identifier=1859,
        id_text="GD_Challenges.Economy.General_MoneyFromCashDrops",
        category=challenge_cat_money,
        name="Dolla Dolla Bills, Y'all",
        description="Collect dollars from cash drops",
        levels=(5000, 25000, 125000, 500000, 1000000),
    )
    challenges[1678] = create_bl2_challenge_that_is_accepted(
        position=112,
        identifier=1678,
        id_text="GD_Challenges.Economy.Economy_SellItems",
        category=challenge_cat_money,
        name="Wholesale",
        description="Sell items to vending machines",
        levels=(10, 25, 150, 300, 750),
    )
    challenges[1860] = create_bl2_challenge_that_is_accepted(
        position=113,
        identifier=1860,
        id_text="GD_Challenges.Economy.Economy_PurchaseItemsOfTheDay",
        category=challenge_cat_money,
        name="Limited-Time Offer",
        description="Buy Items of the Day",
        levels=(1, 5, 15, 30, 50),
    )
    challenges[1810] = create_bl2_challenge_that_is_accepted(
        position=111,
        identifier=1810,
        id_text="GD_Challenges.Economy.Economy_BuyItemsWithEridium",
        category=challenge_cat_money,
        name="Whaddaya Buyin'?",
        description="Purchase items with Eridium",
        levels=(2, 5, 9, 14, 20),
        bonus=4,
    )
    challenges[1805] = create_bl2_challenge_that_is_accepted(
        position=214,
        identifier=1805,
        id_text="GD_Challenges.Economy.Trade_ItemsWithPlayers",
        category=challenge_cat_money,
        name="Psst, Hey Buddy...",
        description="Trade with other players",
        levels=(1, 5, 15, 30, 50),
    )

    # Vehicle
    challenges[1640] = create_bl2_challenge_that_is_accepted(
        position=37,
        identifier=1640,
        id_text="GD_Challenges.Vehicles.Vehicles_KillByRamming",
        category=challenge_cat_vehicle,
        name="Hit-and-Fun",
        description="Kill enemies by ramming them with a vehicle",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1920] = create_bl2_challenge_that_is_accepted(
        position=275,
        identifier=1920,
        id_text="GD_Challenges.Vehicles.Vehicles_KillByPowerSlide",
        category=challenge_cat_vehicle,
        name="Blue Sparks",
        description="Kill enemies by power-sliding over them in a vehicle",
        levels=(5, 15, 30, 50, 75),
        bonus=3,
    )
    challenges[1641] = create_bl2_challenge_that_is_accepted(
        position=38,
        identifier=1641,
        id_text="GD_Challenges.Vehicles.Vehicles_KillsWithVehicleWeapon",
        category=challenge_cat_vehicle,
        name="Turret Syndrome",
        description="Kill enemies using a turret or vehicle-mounted weapon",
        levels=(10, 25, 150, 300, 750),
    )
    challenges[1922] = create_bl2_challenge_that_is_accepted(
        position=277,
        identifier=1922,
        id_text="GD_Challenges.Vehicles.Vehicles_VehicleKillsVehicle",
        category=challenge_cat_vehicle,
        name="...One Van Leaves",
        description="Kill vehicles while in a vehicle",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1919] = create_bl2_challenge_that_is_accepted(
        position=274,
        identifier=1919,
        id_text="GD_Challenges.Vehicles.Vehicles_KillsWhilePassenger",
        category=challenge_cat_vehicle,
        name="Passive Aggressive",
        description="Kill enemies while riding as a passenger (not a gunner) in a vehicle",
        levels=(1, 10, 50, 100, 200),
    )

    # Health
    challenges[1917] = create_bl2_challenge_that_is_accepted(
        position=270,
        identifier=1917,
        id_text="GD_Challenges.Player.Player_PointsHealed",
        category=challenge_cat_health,
        name="Heal Plz",
        description="Recover health",
        levels=(1000, 25000, 150000, 1000000, 5000000),
    )
    challenges[1865] = create_bl2_challenge_that_is_accepted(
        position=200,
        identifier=1865,
        id_text="GD_Challenges.Player.Player_SecondWind",
        category=challenge_cat_health,
        name="I'll Just Help Myself",
        description="Get Second Winds by killing an enemy",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1866] = create_bl2_challenge_that_is_accepted(
        position=201,
        identifier=1866,
        id_text="GD_Challenges.Player.Player_SecondWindFromBadass",
        category=challenge_cat_health,
        name="Badass Bingo",
        description="Get Second Winds by killing a badass enemy",
        levels=(1, 5, 15, 30, 50),
        bonus=5,
    )
    challenges[1868] = create_bl2_challenge_that_is_accepted(
        position=204,
        identifier=1868,
        id_text="GD_Challenges.Player.Player_CoopRevivesOfFriends",
        category=challenge_cat_health,
        name="This Is No Time for Lazy!",
        description="Revive a co-op partner",
        levels=(5, 10, 50, 100, 200),
        bonus=5,
    )
    challenges[1834] = create_bl2_challenge_that_is_accepted(
        position=198,
        identifier=1834,
        id_text="GD_Challenges.Player.Player_SecondWindFromFire",
        category=challenge_cat_health,
        name="Death, Wind, and Fire",
        description="Get Second Winds by killing enemies with a burn DoT (damage over time)",
        levels=(1, 5, 15, 30, 50),
    )
    challenges[1833] = create_bl2_challenge_that_is_accepted(
        position=197,
        identifier=1833,
        id_text="GD_Challenges.Player.Player_SecondWindFromCorrosive",
        category=challenge_cat_health,
        name="Green Meanie",
        description="Get Second Winds by killing enemies with a corrosive DoT (damage over time)",
        levels=(1, 5, 15, 30, 50),
    )
    challenges[1835] = create_bl2_challenge_that_is_accepted(
        position=199,
        identifier=1835,
        id_text="GD_Challenges.Player.Player_SecondWindFromShock",
        category=challenge_cat_health,
        name="I'm Back! Shocked?",
        description="Get Second Winds by killing enemies with an electrocute DoT (damage over time)",
        levels=(1, 5, 15, 30, 50),
    )

    # Grenades
    challenges[1639] = create_bl2_challenge_that_is_accepted(
        position=31,
        identifier=1639,
        id_text="GD_Challenges.Grenades.Grenade_Kills",
        category=challenge_cat_grenades,
        name="Pull the Pin",
        description="Kill enemies with grenades",
        levels=(10, 25, 150, 300, 750),
        bonus=3,
    )
    challenges[1886] = create_bl2_challenge_that_is_accepted(
        position=238,
        identifier=1886,
        id_text="GD_Challenges.Grenades.Grenade_KillsSingularityType",
        category=challenge_cat_grenades,
        name="Singled Out",
        description="Kill enemies with Singularity grenades",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1885] = create_bl2_challenge_that_is_accepted(
        position=237,
        identifier=1885,
        id_text="GD_Challenges.Grenades.Grenade_KillsMirvType",
        category=challenge_cat_grenades,
        name="EXPLOOOOOSIONS!",
        description="Kill enemies with Mirv grenades",
        levels=(10, 25, 75, 150, 300),
        bonus=3,
    )
    challenges[1883] = create_bl2_challenge_that_is_accepted(
        position=235,
        identifier=1883,
        id_text="GD_Challenges.Grenades.Grenade_KillsAoEoTType",
        category=challenge_cat_grenades,
        name="Chemical Sprayer",
        description="Kill enemies with Area-of-Effect grenades",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1884] = create_bl2_challenge_that_is_accepted(
        position=236,
        identifier=1884,
        id_text="GD_Challenges.Grenades.Grenade_KillsBouncing",
        category=challenge_cat_grenades,
        name="Whoa, Black Betty",
        description="Kill enemies with Bouncing Betty grenades",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1918] = create_bl2_challenge_that_is_accepted(
        position=239,
        identifier=1918,
        id_text="GD_Challenges.Grenades.Grenade_KillsTransfusionType",
        category=challenge_cat_grenades,
        name="Health Vampire",
        description="Kill enemies with Transfusion grenades",
        levels=(10, 25, 75, 150, 300),
    )

    # Shields
    challenges[1889] = create_bl2_challenge_that_is_accepted(
        position=243,
        identifier=1889,
        id_text="GD_Challenges.Shields.Shields_KillsNova",
        category=challenge_cat_shields,
        name="Super Novas",
        description="Kill enemies with a Nova shield burst",
        levels=(5, 10, 50, 100, 200),
        bonus=3,
    )
    challenges[1890] = create_bl2_challenge_that_is_accepted(
        position=244,
        identifier=1890,
        id_text="GD_Challenges.Shields.Shields_KillsRoid",
        category=challenge_cat_shields,
        name="Roid Rage",
        description='Kill enemies while buffed by a "Maylay" shield',
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1891] = create_bl2_challenge_that_is_accepted(
        position=245,
        identifier=1891,
        id_text="GD_Challenges.Shields.Shields_KillsSpikes",
        category=challenge_cat_shields,
        name="Game of Thorns",
        description="Kill enemies with reflected damage from a Spike shield",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1892] = create_bl2_challenge_that_is_accepted(
        position=246,
        identifier=1892,
        id_text="GD_Challenges.Shields.Shields_KillsImpact",
        category=challenge_cat_shields,
        name="Amp It Up",
        description="Kill enemies while buffed by an Amplify shield",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1930] = create_bl2_challenge_that_is_accepted(
        position=222,
        identifier=1930,
        id_text="GD_Challenges.Shields.Shields_AbsorbAmmo",
        category=challenge_cat_shields,
        name="Ammo Eater",
        description="Absorb enemy ammo with an Absorption shield",
        levels=(20, 75, 250, 600, 1000),
        bonus=5,
    )

    # Rocket Launchers
    challenges[1762] = create_bl2_challenge_that_is_accepted(
        position=32,
        identifier=1762,
        id_text="GD_Challenges.Weapons.Launcher_Kills",
        category=challenge_cat_rockets,
        name="Rocket and Roll",
        description="Kill enemies with rocket launchers",
        levels=(10, 50, 100, 250, 500),
        bonus=3,
    )
    challenges[1828] = create_bl2_challenge_that_is_accepted(
        position=192,
        identifier=1828,
        id_text="GD_Challenges.Weapons.Launcher_SecondWinds",
        category=challenge_cat_rockets,
        name="Gone with the Second Wind",
        description="Get Second Winds with rocket launchers",
        levels=(2, 5, 15, 30, 50),
    )
    challenges[1870] = create_bl2_challenge_that_is_accepted(
        position=224,
        identifier=1870,
        id_text="GD_Challenges.Weapons.Launcher_KillsSplashDamage",
        category=challenge_cat_rockets,
        name="Splish Splash",
        description="Kill enemies with rocket launcher splash damage",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1869] = create_bl2_challenge_that_is_accepted(
        position=223,
        identifier=1869,
        id_text="GD_Challenges.Weapons.Launcher_KillsDirectHit",
        category=challenge_cat_rockets,
        name="Catch-a-Rocket!",
        description="Kill enemies with direct hits from rocket launchers",
        levels=(5, 10, 50, 100, 200),
        bonus=5,
    )
    challenges[1871] = create_bl2_challenge_that_is_accepted(
        position=54,
        identifier=1871,
        id_text="GD_Challenges.Weapons.Launcher_KillsFullShieldEnemy",
        category=challenge_cat_rockets,
        name="Shield Basher",
        description="Kill shielded enemies with one rocket each",
        levels=(5, 15, 35, 75, 125),
    )
    challenges[1808] = create_bl2_challenge_that_is_accepted(
        position=52,
        identifier=1808,
        id_text="GD_Challenges.Weapons.Launcher_KillsLongRange",
        category=challenge_cat_rockets,
        name="Sky Rockets in Flight...",
        description="Kill enemies from long range with rocket launchers",
        levels=(25, 100, 400, 1000, 2000),
    )

    # Sniper Rifles
    challenges[1636] = create_bl2_challenge_that_is_accepted(
        position=28,
        identifier=1636,
        id_text="GD_Challenges.Weapons.SniperRifle_Kills",
        category=challenge_cat_sniper,
        name="Longshot",
        description="Kill enemies with sniper rifles",
        levels=(20, 100, 500, 2500, 5000),
        bonus=3,
    )
    challenges[1666] = create_bl2_challenge_that_is_accepted(
        position=178,
        identifier=1666,
        id_text="GD_Challenges.Weapons.Sniper_CriticalHits",
        category=challenge_cat_sniper,
        name="Longshot Headshot",
        description="Get critical hits with sniper rifles",
        levels=(25, 100, 400, 1000, 2000),
    )
    challenges[1824] = create_bl2_challenge_that_is_accepted(
        position=188,
        identifier=1824,
        id_text="GD_Challenges.Weapons.Sniper_SecondWinds",
        category=challenge_cat_sniper,
        name="Leaf on the Second Wind",
        description="Get Second Winds with sniper rifles",
        levels=(2, 5, 15, 30, 50),
    )
    challenges[1844] = create_bl2_challenge_that_is_accepted(
        position=59,
        identifier=1844,
        id_text="GD_Challenges.Weapons.Sniper_CriticalHitKills",
        category=challenge_cat_sniper,
        name="Snipe Hunting",
        description="Kill enemies with critical hits using sniper rifles",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1798] = create_bl2_challenge_that_is_accepted(
        position=47,
        identifier=1798,
        id_text="GD_Challenges.Weapons.SniperRifle_KillsFromHip",
        category=challenge_cat_sniper,
        name="No Scope, No Problem",
        description="Kill enemies with sniper rifles without using ironsights",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1881] = create_bl2_challenge_that_is_accepted(
        position=233,
        identifier=1881,
        id_text="GD_Challenges.Weapons.SniperRifle_KillsUnaware",
        category=challenge_cat_sniper,
        name="Surprise!",
        description="Kill unaware enemies with sniper rifles",
        levels=(5, 10, 50, 100, 200),
    )
    challenges[1872] = create_bl2_challenge_that_is_accepted(
        position=55,
        identifier=1872,
        id_text="GD_Challenges.Weapons.SniperRifle_KillsFullShieldEnemy",
        category=challenge_cat_sniper,
        name="Eviscerated",
        description="Kill shielded enemies with one shot using sniper rifles",
        levels=(5, 15, 35, 75, 125),
        bonus=5,
    )

    # Assault Rifles
    challenges[1637] = create_bl2_challenge_that_is_accepted(
        position=29,
        identifier=1637,
        id_text="GD_Challenges.Weapons.AssaultRifle_Kills",
        category=challenge_cat_ar,
        name="Aggravated Assault",
        description="Kill enemies with assault rifles",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )
    challenges[1667] = create_bl2_challenge_that_is_accepted(
        position=179,
        identifier=1667,
        id_text="GD_Challenges.Weapons.AssaultRifle_CriticalHits",
        category=challenge_cat_ar,
        name="This Is My Rifle...",
        description="Get critical hits with assault rifles",
        levels=(25, 100, 400, 1000, 2000),
    )
    challenges[1825] = create_bl2_challenge_that_is_accepted(
        position=189,
        identifier=1825,
        id_text="GD_Challenges.Weapons.AssaultRifle_SecondWinds",
        category=challenge_cat_ar,
        name="From My Cold, Dead Hands",
        description="Get Second Winds with assault rifles",
        levels=(5, 15, 30, 50, 75),
    )
    challenges[1845] = create_bl2_challenge_that_is_accepted(
        position=60,
        identifier=1845,
        id_text="GD_Challenges.Weapons.AssaultRifle_CriticalHitKills",
        category=challenge_cat_ar,
        name="...This Is My Gun",
        description="Kill enemies with critical hits using assault rifles",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1797] = create_bl2_challenge_that_is_accepted(
        position=46,
        identifier=1797,
        id_text="GD_Challenges.Weapons.AssaultRifle_KillsCrouched",
        category=challenge_cat_ar,
        name="Crouching Tiger, Hidden Assault Rifle",
        description="Kill enemies with assault rifles while crouched",
        levels=(25, 75, 400, 1600, 3200),
        bonus=5,
    )

    # SMGs
    challenges[1635] = create_bl2_challenge_that_is_accepted(
        position=27,
        identifier=1635,
        id_text="GD_Challenges.Weapons.SMG_Kills",
        category=challenge_cat_smg,
        name="Hail of Bullets",
        description="Kill enemies with SMGs",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )
    challenges[1665] = create_bl2_challenge_that_is_accepted(
        position=177,
        identifier=1665,
        id_text="GD_Challenges.Weapons.SMG_CriticalHits",
        category=challenge_cat_smg,
        name="Constructive Criticism",
        description="Get critical hits with SMGs",
        levels=(25, 100, 400, 1000, 2000),
    )
    challenges[1843] = create_bl2_challenge_that_is_accepted(
        position=58,
        identifier=1843,
        id_text="GD_Challenges.Weapons.SMG_CriticalHitKills",
        category=challenge_cat_smg,
        name="High Rate of Ire",
        description="Kill enemies with critical hits using SMGs",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1823] = create_bl2_challenge_that_is_accepted(
        position=187,
        identifier=1823,
        id_text="GD_Challenges.Weapons.SMG_SecondWinds",
        category=challenge_cat_smg,
        name="More Like Submachine FUN",
        description="Get Second Winds with SMGs",
        levels=(2, 5, 15, 30, 50),
    )

    # Shotguns
    challenges[1634] = create_bl2_challenge_that_is_accepted(
        position=26,
        identifier=1634,
        id_text="GD_Challenges.Weapons.Shotgun_Kills",
        category=challenge_cat_shotgun,
        name="Shotgun!",
        description="Kill enemies with shotguns",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )
    challenges[1664] = create_bl2_challenge_that_is_accepted(
        position=176,
        identifier=1664,
        id_text="GD_Challenges.Weapons.Shotgun_CriticalHits",
        category=challenge_cat_shotgun,
        name="Faceful of Buckshot",
        description="Get critical hits with shotguns",
        levels=(50, 250, 1000, 2500, 5000),
    )
    challenges[1822] = create_bl2_challenge_that_is_accepted(
        position=186,
        identifier=1822,
        id_text="GD_Challenges.Weapons.Shotgun_SecondWinds",
        category=challenge_cat_shotgun,
        name="Lock, Stock, and...",
        description="Get Second Winds with shotguns",
        levels=(2, 5, 15, 30, 50),
    )
    challenges[1806] = create_bl2_challenge_that_is_accepted(
        position=50,
        identifier=1806,
        id_text="GD_Challenges.Weapons.Shotgun_KillsPointBlank",
        category=challenge_cat_shotgun,
        name="Open Wide!",
        description="Kill enemies from point-blank range with shotguns",
        levels=(10, 25, 150, 300, 750),
    )
    challenges[1807] = create_bl2_challenge_that_is_accepted(
        position=51,
        identifier=1807,
        id_text="GD_Challenges.Weapons.Shotgun_KillsLongRange",
        category=challenge_cat_shotgun,
        name="Shotgun Sniper",
        description="Kill enemies from long range with shotguns",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1842] = create_bl2_challenge_that_is_accepted(
        position=57,
        identifier=1842,
        id_text="GD_Challenges.Weapons.Shotgun_CriticalHitKills",
        category=challenge_cat_shotgun,
        name="Shotgun Surgeon",
        description="Kill enemies with critical hits using shotguns",
        levels=(10, 50, 100, 250, 500),
    )

    # Pistols
    challenges[1633] = create_bl2_challenge_that_is_accepted(
        position=25,
        identifier=1633,
        id_text="GD_Challenges.Weapons.Pistol_Kills",
        category=challenge_cat_pistol,
        name="The Killer",
        description="Kill enemies with pistols",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )
    challenges[1663] = create_bl2_challenge_that_is_accepted(
        position=175,
        identifier=1663,
        id_text="GD_Challenges.Weapons.Pistol_CriticalHits",
        category=challenge_cat_pistol,
        name="Deadeye",
        description="Get critical hits with pistols",
        levels=(25, 100, 400, 1000, 2000),
    )
    challenges[1821] = create_bl2_challenge_that_is_accepted(
        position=185,
        identifier=1821,
        id_text="GD_Challenges.Weapons.Pistol_SecondWinds",
        category=challenge_cat_pistol,
        name="Hard Boiled",
        description="Get Second Winds with pistols",
        levels=(2, 5, 15, 30, 50),
    )
    challenges[1841] = create_bl2_challenge_that_is_accepted(
        position=56,
        identifier=1841,
        id_text="GD_Challenges.Weapons.Pistol_CriticalHitKills",
        category=challenge_cat_pistol,
        name="Pistolero",
        description="Kill enemies with critical hits using pistols",
        levels=(10, 25, 75, 150, 300),
    )
    challenges[1800] = create_bl2_challenge_that_is_accepted(
        position=49,
        identifier=1800,
        id_text="GD_Challenges.Weapons.Pistol_KillsQuickshot",
        category=challenge_cat_pistol,
        name="Quickdraw",
        description="Kill enemies shortly after entering ironsights with a pistol",
        levels=(10, 25, 150, 300, 750),
        bonus=5,
    )

    # Melee
    challenges[1650] = create_bl2_challenge_that_is_accepted(
        position=75,
        identifier=1650,
        id_text="GD_Challenges.Melee.Melee_Kills",
        category=challenge_cat_melee,
        name="Fisticuffs!",
        description="Kill enemies with melee attacks",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )
    challenges[1893] = create_bl2_challenge_that_is_accepted(
        position=247,
        identifier=1893,
        id_text="GD_Challenges.Melee.Melee_KillsBladed",
        category=challenge_cat_melee,
        name="A Squall of Violence",
        description="Kill enemies with melee attacks using bladed guns",
        levels=(20, 75, 250, 600, 1000),
    )

    # General Combat
    challenges[1621] = create_bl2_challenge_that_is_accepted(
        position=0,
        identifier=1621,
        id_text="GD_Challenges.GeneralCombat.General_RoundsFired",
        category=challenge_cat_combat,
        name="Knee-Deep in Brass",
        description="Fire a lot of rounds",
        levels=(1000, 5000, 10000, 25000, 50000),
        bonus=5,
    )
    challenges[1702] = create_bl2_challenge_that_is_accepted(
        position=90,
        identifier=1702,
        id_text="GD_Challenges.GeneralCombat.Player_KillsWithActionSkill",
        category=challenge_cat_combat,
        name="...To Pay the Bills",
        description="Kill enemies while using your Action Skill",
        levels=(20, 75, 250, 600, 1000),
        bonus=5,
    )
    challenges[1916] = create_bl2_challenge_that_is_accepted(
        position=269,
        identifier=1916,
        id_text="GD_Challenges.GeneralCombat.Kills_AtNight",
        category=challenge_cat_combat,
        name="...I Got to Boogie",
        description="Kill enemies at night",
        levels=(10, 25, 150, 300, 750),
    )
    challenges[1915] = create_bl2_challenge_that_is_accepted(
        position=268,
        identifier=1915,
        id_text="GD_Challenges.GeneralCombat.Kills_AtDay",
        category=challenge_cat_combat,
        name="Afternoon Delight",
        description="Kill enemies during the day",
        levels=(50, 250, 1000, 2500, 5000),
    )
    challenges[1908] = create_bl2_challenge_that_is_accepted(
        position=261,
        identifier=1908,
        id_text="GD_Challenges.GeneralCombat.Tediore_KillWithReload",
        category=challenge_cat_combat,
        name="Boomerbang",
        description="Kill enemies with Tediore reloads",
        levels=(5, 10, 50, 100, 200),
        bonus=5,
    )
    challenges[1909] = create_bl2_challenge_that_is_accepted(
        position=262,
        identifier=1909,
        id_text="GD_Challenges.GeneralCombat.Tediore_DamageFromReloads",
        category=challenge_cat_combat,
        name="Gun Slinger",
        description="Deal damage with Tediore reloads",
        levels=(5000, 20000, 100000, 500000, 1000000),
    )
    challenges[1912] = create_bl2_challenge_that_is_accepted(
        position=265,
        identifier=1912,
        id_text="GD_Challenges.GeneralCombat.Barrels_KillEnemies",
        category=challenge_cat_combat,
        name="Not Full of Monkeys",
        description="Kill enemies with stationary barrels",
        levels=(10, 25, 45, 70, 100),
        bonus=3,
    )
    challenges[1646] = create_bl2_challenge_that_is_accepted(
        position=44,
        identifier=1646,
        id_text="GD_Challenges.GeneralCombat.Kills_FromCrits",
        category=challenge_cat_combat,
        name="Critical Acclaim",
        description="Kill enemies with critical hits. And rainbows.",
        levels=(20, 100, 500, 1000, 1500),
    )

    # Miscellaneous
    challenges[1659] = create_bl2_challenge_that_is_accepted(
        position=104,
        identifier=1659,
        id_text="GD_Challenges.Dueling.DuelsWon_HatersGonnaHate",
        category=challenge_cat_misc,
        name="Haters Gonna Hate",
        description="Win duels",
        levels=(1, 5, 15, 30, 50),
    )
    challenges[1804] = create_bl2_challenge_that_is_accepted(
        position=211,
        identifier=1804,
        id_text="GD_Challenges.Miscellaneous.Missions_SideMissionsCompleted",
        category=challenge_cat_misc,
        name="Sidejacked",
        description="Complete side missions",
        levels=(5, 15, 30, 55, 90),
    )
    challenges[1803] = create_bl2_challenge_that_is_accepted(
        position=210,
        identifier=1803,
        id_text="GD_Challenges.Miscellaneous.Missions_OptionalObjectivesCompleted",
        category=challenge_cat_misc,
        name="Compl33tionist",
        description="Complete optional mission objectives",
        levels=(10, 25, 45, 70, 100),
    )
    challenges[1698] = create_bl2_challenge_that_is_accepted(
        position=173,
        identifier=1698,
        id_text="GD_Challenges.Miscellaneous.Misc_CompleteChallenges",
        category=challenge_cat_misc,
        name="Yo Dawg I Herd You Like Challenges",
        description="Complete many, many challenges",
        levels=(5, 25, 50, 100, 200),
    )
    challenges[1940] = create_bl2_challenge_that_is_accepted(
        position=100,
        identifier=1940,
        id_text="GD_Challenges.Miscellaneous.Misc_JimmyJenkins",
        category=challenge_cat_misc,
        name="JEEEEENKINSSSSSS!!!",
        description="Find and eliminate Jimmy Jenkins",
        levels=(1, 3, 6, 10, 15),
        bonus=5,
    )

    return challenges
