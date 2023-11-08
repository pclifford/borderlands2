from typing import Final, Dict

from borderlands.challenges import Challenge, ChallengeCategory

# NOTE: unused now
LEVELS_TO_TRAVEL_STATION_MAP: Final = {
    'Access_P': "Tycho's Ribs",
    'CentralTerminal_P': "Hyperion Hub of Heroism",
    'ComFacility_P': "Crisis Scar",
    'DahlFactory_Boss': "Titan Robot Production Plant",
    'DahlFactory_P': "Titan Industrial Facility",
    'Deadsurface_P': "Regolith Range",
    'Digsite_P': "Vorago Solitude",
    'Digsite_Rk5arena_P': "Outfall Pumping Station",
    'Eridian_Slaughter_P': "Holodome",
    'InnerCore_P': "Eleseer",
    'InnerHull_P': "Veins of Helios",
    'JacksOffice_P': "Jack's Office",
    'Laser_P': "Lunar Launching Station",
    'LaserBoss_P': "Eye of Helios",
    'Ma_Deck13_P': "Deck 13 1/2",
    'Ma_FinalBoss_P': "Deck 13.5",
    'Ma_LeftCluster_P': "Cluster 00773 P4ND0R4",
    'Ma_Motherboard_P': "Motherlessboard",
    'Ma_Nexus_P': "Nexus",
    'Ma_RightCluster_P': "Cluster 99002 0V3RL00K",
    'Ma_SubBoss_P': "Cortex",
    'Ma_Subconscious_P': "Subconscious",
    'Meriff_P': "Meriff's Office",
    'Moon_P': "Triton Flats",
    'MoonShotIntro_P': "Helios Station",
    'MoonSlaughter_P': "Abandoned Training Facility",
    'Moonsurface_P': "Serenity's Waste",
    'Outlands_P': "Outlands Spur",
    'Outlands_P2': "Outlands Canyon",
    'RandDFacility_P': "Research and Development",
    'Spaceport_P': "Concordia",
    'StantonsLiver_P': "Stanton's Liver",
    'Sublevel13_P': "Sub-Level 13",
    'Wreck_P': "Pity's Fall",
}


def create_bltps_challenges() -> Dict[int, Challenge]:
    # Challenge categories
    challenge_cat_gravity = ChallengeCategory("Low Gravity")
    challenge_cat_grinder = ChallengeCategory("Grinder")
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
    challenge_cat_laser = ChallengeCategory("Laser")
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
    #
    # New major DLC for TPS seems unlikely too, though time will tell.
    # noinspection PyDictCreation
    challenges = {}

    # Low Gravity
    challenges[2052] = Challenge(
        position=468,
        identifier=2052,
        id_text="GD_Challenges.LowGravity.LowGravity_CriticalsWhileAirborne",
        category=challenge_cat_gravity,
        name="Eagle Eye",
        description="Get critical hits while airborne",
        levels=(50, 250, 500, 1500, 3000),
    )

    challenges[2093] = Challenge(
        position=507,
        identifier=2093,
        id_text="GD_Challenges.LowGravity.LowGravity_DoubleJump",
        category=challenge_cat_gravity,
        name="Boosted",
        description="Perform air boosts",
        levels=(50, 250, 1000, 2500, 5000),
    )

    challenges[2051] = Challenge(
        position=467,
        identifier=2051,
        id_text="GD_Challenges.LowGravity.LowGravity_KillsWhileAirborne",
        category=challenge_cat_gravity,
        name="Death from Above",
        description="Kill enemies while in the air",
        levels=(50, 250, 1000, 2500, 5000),
        bonus=5,
    )

    challenges[2055] = Challenge(
        position=471,
        identifier=2055,
        id_text="GD_Challenges.LowGravity.LowGravity_KillsWithSlam",
        category=challenge_cat_gravity,
        name="Slampage!",
        description="Kill enemies with slam attacks",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[2053] = Challenge(
        position=469,
        identifier=2053,
        id_text="GD_Challenges.LowGravity.LowGravity_MeleeWhileAirborne",
        category=challenge_cat_gravity,
        name="Dragon Punch",
        description="Deal melee damage while airborne",
        levels=(5000, 10000, 25000, 75000, 200000),
    )

    challenges[2054] = Challenge(
        position=470,
        identifier=2054,
        id_text="GD_Challenges.LowGravity.LowGravity_SlamDamage",
        category=challenge_cat_gravity,
        name="Roger Slamjet",
        description="Desc",
        levels=(2000, 10000, 50000, 100000, 2500000),
    )

    # Grinder
    challenges[2060] = Challenge(
        position=476,
        identifier=2060,
        id_text="GD_Challenges.Grinder.Grinder_GrinderRecipes",
        category=challenge_cat_grinder,
        name="Master Chef",
        description="Discover Grinder recipes",
        levels=(2, 5, 10, 20, 34),
        bonus=3,
    )

    challenges[2061] = Challenge(
        position=477,
        identifier=2061,
        id_text="GD_Challenges.Grinder.Grinder_MoonstoneAttachments",
        category=challenge_cat_grinder,
        name="Greater Than the Sum of its Parts",
        description="Obtain Luneshine weapons from the Grinder",
        levels=(20, 50, 75, 125, 200),
    )

    challenges[2059] = Challenge(
        position=475,
        identifier=2059,
        id_text="GD_Challenges.Grinder.Grinder_MoonstoneGrind",
        category=challenge_cat_grinder,
        name="This Time for Sure",
        description="Perform Moonstone grinds",
        levels=(10, 25, 150, 300, 750),
    )

    challenges[2058] = Challenge(
        position=474,
        identifier=2058,
        id_text="GD_Challenges.Grinder.Grinder_StandardGrind",
        category=challenge_cat_grinder,
        name="The Daily Grind",
        description="Perform standard grind",
        levels=(50, 250, 750, 1500, 25000),
    )

    # Enemies
    challenges[2035] = Challenge(
        position=452,
        identifier=2035,
        id_text="GD_Challenges.Enemies.Enemies_KillDahlBadasses",
        category=challenge_cat_enemies,
        name="Kiss My Badass",
        description="Kill Lost Legion badasses",
        levels=(5, 10, 20, 30, 50),
    )

    challenges[2028] = Challenge(
        position=445,
        identifier=2028,
        id_text="GD_Challenges.Enemies.Enemies_KillDahlFlyers",
        category=challenge_cat_enemies,
        name="Crash & Burn",
        description="Destroy Lost Legion jet fighters",
        levels=(1, 3, 5, 10, 20),
        bonus=3,
    )

    challenges[2027] = Challenge(
        position=444,
        identifier=2027,
        id_text="GD_Challenges.Enemies.Enemies_KillDahlInfantry",
        category=challenge_cat_enemies,
        name="Get Some!",
        description="Kill Lost Legion infantry",
        levels=(50, 250, 500, 1000, 2000),
    )

    challenges[2029] = Challenge(
        position=446,
        identifier=2029,
        id_text="GD_Challenges.Enemies.Enemies_KillDahlSuits",
        category=challenge_cat_enemies,
        name="No Suit for You!",
        description="Kill Lost Legion powersuits",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[2043] = Challenge(
        position=460,
        identifier=2043,
        id_text="GD_Challenges.Enemies.Enemies_KillGuardianBosses",
        category=challenge_cat_enemies,
        name="More Where That Came From",
        description="Kill Eridian Guardian bosses",
        levels=(2, 4, 6, 8, 10),
        bonus=3,
    )

    challenges[2031] = Challenge(
        position=448,
        identifier=2031,
        id_text="GD_Challenges.Enemies.Enemies_KillGuardians",
        category=challenge_cat_enemies,
        name="Not So Tough Now",
        description="Kill Eridian Guardians",
        levels=(25, 50, 100, 150, 250),
    )

    challenges[2030] = Challenge(
        position=447,
        identifier=2030,
        id_text="GD_Challenges.Enemies.Enemies_KillHyperionInfantry",
        category=challenge_cat_enemies,
        name="Dose of Death",
        description="Kill enemies infected with space hurps",
        levels=(10, 50, 125, 250, 500),
    )

    challenges[2034] = Challenge(
        position=451,
        identifier=2034,
        id_text="GD_Challenges.Enemies.Enemies_KillKraggonBadasses",
        category=challenge_cat_enemies,
        name="Slayer of Titans",
        description="Kill kraggon badasses",
        levels=(1, 3, 7, 15, 25),
        bonus=3,
    )

    challenges[2032] = Challenge(
        position=449,
        identifier=2032,
        id_text="GD_Challenges.Enemies.Enemies_KillKraggons",
        category=challenge_cat_enemies,
        name="Big Game Hunt",
        description="Kill kraggons",
        levels=(25, 50, 150, 300, 750),
    )

    challenges[2039] = Challenge(
        position=456,
        identifier=2039,
        id_text="GD_Challenges.Enemies.Enemies_KillLunarLooters",
        category=challenge_cat_enemies,
        name="Gift That Keeps Giving",
        description="Kill swagmen",
        levels=(1, 3, 5, 8, 12),
    )

    challenges[1989] = Challenge(
        position=406,
        identifier=1989,
        id_text="GD_Challenges.Enemies.Enemies_KillRathyds",
        category=challenge_cat_enemies,
        name="Exterminator",
        description="Kill rathyds",
        levels=(25, 50, 150, 300, 750),
    )

    challenges[2038] = Challenge(
        position=455,
        identifier=2038,
        id_text="GD_Challenges.Enemies.Enemies_KillScavBadasses",
        category=challenge_cat_enemies,
        name="The One That Says B.A.M.F.",
        description="Kill scav badasses",
        levels=(10, 25, 50, 100, 250),
    )

    challenges[2037] = Challenge(
        position=454,
        identifier=2037,
        id_text="GD_Challenges.Enemies.Enemies_KillScavFlyers",
        category=challenge_cat_enemies,
        name="It Wasn't Yours, Anyway",
        description="Destroy scav jet fighters",
        levels=(1, 3, 5, 10, 20),
    )

    challenges[2036] = Challenge(
        position=453,
        identifier=2036,
        id_text="GD_Challenges.Enemies.Enemies_KillScavSpacemen",
        category=challenge_cat_enemies,
        name="Space Dead",
        description="Kill scav outlaws",
        levels=(25, 50, 150, 300, 750),
        bonus=3,
    )

    challenges[2033] = Challenge(
        position=450,
        identifier=2033,
        id_text="GD_Challenges.Enemies.Enemies_KillScavs",
        category=challenge_cat_enemies,
        name="Die, Moon Jerks",
        description="Kill scavs",
        levels=(75, 250, 750, 2000, 5000),
    )

    challenges[1988] = Challenge(
        position=405,
        identifier=1988,
        id_text="GD_Challenges.Enemies.Enemies_KillShugguraths",
        category=challenge_cat_enemies,
        name="That Was Unpleasant",
        description="Kill shugguraths",
        levels=(25, 50, 150, 300, 750),
    )

    challenges[2041] = Challenge(
        position=458,
        identifier=2041,
        id_text="GD_Challenges.Enemies.Enemies_KillTorkBadasses",
        category=challenge_cat_enemies,
        name="Torkin' Out the Trash",
        description="Kill tork badasses",
        levels=(5, 10, 20, 30, 50),
    )

    challenges[1974] = Challenge(
        position=391,
        identifier=1974,
        id_text="GD_Challenges.Enemies.Enemies_KillTorks",
        category=challenge_cat_enemies,
        name="Pest Control",
        description="Kill torks",
        levels=(25, 75, 150, 500, 1000),
    )

    # This challenge ID is odd, since it identifies itself as a level-specific
    # challenge, but lives up in the "Enemies" section along with everything
    # else.  Unlocking this challenge prematurely will correctly show the
    # challenge in the Enemies section, but will also cause an "Eleseer" entry
    # to be added to the location-specific area, and a single (undiscovered)
    # entry will be there.  TODO: I have yet to verify that that doesn't
    # cause problems when you do first enter Eleseer.  I assume it should be
    # fine, though I should doublecheck.
    challenges[2257] = Challenge(
        position=671,
        identifier=2257,
        id_text="GD_Challenges.Co_LevelChallenges.InnerCore_AintNobodyGotTime",
        category=challenge_cat_enemies,
        name="Aim for the Little Ones",
        description="Kill Opha's spawned Putti",
        levels=(10, 25, 45, 70, 100),
    )

    challenges[1728] = Challenge(
        position=331,
        identifier=1728,
        id_text="GD_Marigold_Challenges.Enemies.Enemies_KillCorruptions",
        category=challenge_cat_enemies,
        name="Clean Sweep",
        description="Kill corrupted enemies inside of Claptrap",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1727] = Challenge(
        position=330,
        identifier=1727,
        id_text="GD_Marigold_Challenges.Enemies.Enemies_KillInsecuityForces",
        category=challenge_cat_enemies,
        name="Claptomaniac",
        description="Kill insecurity forces",
        levels=(5, 10, 25, 75, 200),
        bonus=3,
    )

    challenges[1733] = Challenge(
        position=336,
        identifier=1733,
        id_text="GD_Marigold_Challenges.Enemies.Enemies_KillsFromBitBombs",
        category=challenge_cat_enemies,
        name="Volakillity",
        description="Kill enemies with Volatile Bits",
        levels=(3, 8, 20, 50, 120),
    )

    # Elemental
    challenges[1823] = Challenge(
        position=226,
        identifier=1823,
        id_text="GD_Challenges.elemental.Elemental_SetEnemiesOnFire",
        category=challenge_cat_elemental,
        name="Way of the Enkindling",
        description="Light enemies on fire",
        levels=(25, 100, 400, 1000, 2000),
    )

    challenges[1592] = Challenge(
        position=40,
        identifier=1592,
        id_text="GD_Challenges.elemental.Elemental_KillEnemiesCorrosive",
        category=challenge_cat_elemental,
        name="Toxic Takedown",
        description="Kill enemies with corrosive damage",
        levels=(20, 75, 250, 600, 1000),
    )

    challenges[1595] = Challenge(
        position=43,
        identifier=1595,
        id_text="GD_Challenges.elemental.Elemental_KillEnemiesExplosive",
        category=challenge_cat_elemental,
        name="Out with a Bang",
        description="Kill enemies with explosive damage",
        levels=(20, 75, 250, 600, 1000),
    )

    challenges[1827] = Challenge(
        position=230,
        identifier=1827,
        id_text="GD_Challenges.elemental.Elemental_DealFireDOTDamage",
        category=challenge_cat_elemental,
        name="Some Like It Hot",
        description="Deal damage with incindiary DoT (damage-over-time) effects",
        levels=(2500, 20000, 100000, 500000, 1000000),
        bonus=5,
    )

    challenges[1828] = Challenge(
        position=231,
        identifier=1828,
        id_text="GD_Challenges.elemental.Elemental_DealCorrosiveDOTDamage",
        category=challenge_cat_elemental,
        name="Chemical Burn",
        description="Deal damage with corrosive DoT (damage-over-time) effects",
        levels=(2500, 20000, 100000, 500000, 1000000),
    )

    challenges[1977] = Challenge(
        position=394,
        identifier=1977,
        id_text="GD_Challenges.elemental.Elemental_DealIceDOTDamage",
        category=challenge_cat_elemental,
        name="Frost Bite",
        description="Deal damage with cryo DoT (damage-over-time) effects",
        levels=(2500, 20000, 100000, 500000, 1000000),
    )

    challenges[1829] = Challenge(
        position=232,
        identifier=1829,
        id_text="GD_Challenges.elemental.Elemental_DealShockDOTDamage",
        category=challenge_cat_elemental,
        name="Watt's Up?",
        description="Deal damage with shock DoT (damage-over-time) effects",
        levels=(5000, 20000, 100000, 500000, 1000000),
    )

    # Loot
    challenges[1848] = Challenge(
        position=252,
        identifier=1848,
        id_text="GD_Challenges.Pickups.Inventory_PickupWhiteItems",
        category=challenge_cat_loot,
        name="Junkyard Dog",
        description="Loot or purchase white items",
        levels=(50, 125, 250, 400, 600),
    )

    challenges[1849] = Challenge(
        position=253,
        identifier=1849,
        id_text="GD_Challenges.Pickups.Inventory_PickupGreenItems",
        category=challenge_cat_loot,
        name="A Chunk of Purest Green",
        description="Loot or purchase green-rarity items",
        levels=(25, 75, 125, 250, 500),
        bonus=3,
    )

    challenges[1850] = Challenge(
        position=254,
        identifier=1850,
        id_text="GD_Challenges.Pickups.Inventory_PickupBlueItems",
        category=challenge_cat_loot,
        name="Rare as Rocking Horse...",
        description="Loot or purchase blue-rarity items",
        levels=(5, 25, 50, 75, 100),
    )

    challenges[1851] = Challenge(
        position=255,
        identifier=1851,
        id_text="GD_Challenges.Pickups.Inventory_PickupPurpleItems",
        category=challenge_cat_loot,
        name="Purple Haze",
        description="Loot or purchase purple-rarity items",
        levels=(3, 7, 15, 30, 75),
    )

    challenges[1852] = Challenge(
        position=256,
        identifier=1852,
        id_text="GD_Challenges.Pickups.Inventory_PickupOrangeItems",
        category=challenge_cat_loot,
        name="The Happiest Color",
        description="Loot or purchase legendary items",
        levels=(1, 3, 6, 10, 15),
        bonus=5,
    )

    challenges[1731] = Challenge(
        position=334,
        identifier=1731,
        id_text="GD_Marigold_Challenges.Loot.Loot_OpenGlitchedChests",
        category=challenge_cat_loot,
        name="I Like Surprises...",
        description="Open Glitched treasure chests",
        levels=(1, 3, 5, 8, 12),
    )

    challenges[1730] = Challenge(
        position=333,
        identifier=1730,
        id_text="GD_Marigold_Challenges.Loot.Loot_PickupGlitchedItems",
        category=challenge_cat_loot,
        name="99 Problems and a Glitch Aint One",
        description="Loot or purchase Glitched-rarity items",
        levels=(1, 3, 6, 10, 15),
        bonus=5,
    )

    challenges[1619] = Challenge(
        position=108,
        identifier=1619,
        id_text="GD_Challenges.Loot.Loot_OpenChests",
        category=challenge_cat_loot,
        name="Aaaaaand OPEN!",
        description="Open treasure chests",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1620] = Challenge(
        position=110,
        identifier=1620,
        id_text="GD_Challenges.Loot.Loot_OpenLootables",
        category=challenge_cat_loot,
        name="Scrounging Around",
        description="Open lootable crates, lockers, and other objects",
        levels=(50, 300, 1000, 2000, 3000),
        bonus=3,
    )

    challenges[1580] = Challenge(
        position=8,
        identifier=1580,
        id_text="GD_Challenges.Loot.Loot_PickUpWeapons",
        category=challenge_cat_loot,
        name="One for Every Occasion",
        description="Pick up or purchase weapons",
        levels=(10, 25, 150, 300, 750),
    )

    # Money
    challenges[1808] = Challenge(
        position=119,
        identifier=1808,
        id_text="GD_Challenges.Economy.Economy_MoneySaved",
        category=challenge_cat_money,
        name="Mom Would Be Proud",
        description="Save a lot of money",
        levels=(10000, 50000, 250000, 1000000, 3000000),
    )

    challenges[1809] = Challenge(
        position=120,
        identifier=1809,
        id_text="GD_Challenges.Economy.General_MoneyFromCashDrops",
        category=challenge_cat_money,
        name="Mr. Money Pits",
        description="Collect dollars from cash drops",
        levels=(5000, 25000, 125000, 500000, 1000000),
    )

    challenges[1628] = Challenge(
        position=113,
        identifier=1628,
        id_text="GD_Challenges.Economy.Economy_SellItems",
        category=challenge_cat_money,
        name="Pawn Broker",
        description="Sell items to vending machines",
        levels=(50, 100, 250, 750, 2000),
    )

    challenges[1810] = Challenge(
        position=114,
        identifier=1810,
        id_text="GD_Challenges.Economy.Economy_PurchaseItemsOfTheDay",
        category=challenge_cat_money,
        name="Impulse Shopper",
        description="Buy Items of the Day from vending machines",
        levels=(1, 5, 15, 30, 50),
    )

    challenges[1760] = Challenge(
        position=112,
        identifier=1760,
        id_text="GD_Challenges.Economy.Economy_BuyItemsWithMoonstone",
        category=challenge_cat_money,
        name="Over the Moon",
        description="Purchase items with Moonstones",
        levels=(25, 50, 125, 250, 500),
        bonus=3,
    )

    challenges[1755] = Challenge(
        position=215,
        identifier=1755,
        id_text="GD_Challenges.Economy.Trade_ItemsWithPlayers",
        category=challenge_cat_money,
        name="Trade Negotiations",
        description="Trade with other players",
        levels=(1, 5, 15, 30, 50),
    )

    # Vehicle
    challenges[1590] = Challenge(
        position=37,
        identifier=1590,
        id_text="GD_Challenges.Vehicles.Vehicles_KillByRamming",
        category=challenge_cat_vehicle,
        name="Fender Bender",
        description="Kill enemies by ramming them with a vehicle",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[1870] = Challenge(
        position=276,
        identifier=1870,
        id_text="GD_Challenges.Vehicles.Vehicles_KillByPowerSlide",
        category=challenge_cat_vehicle,
        name="Splat 'n' Slide",
        description="Kill enemies by power-sliding over them in a vehicle",
        levels=(1, 5, 10, 25, 50),
        bonus=3,
    )

    challenges[1591] = Challenge(
        position=38,
        identifier=1591,
        id_text="GD_Challenges.Vehicles.Vehicles_KillsWithVehicleWeapon",
        category=challenge_cat_vehicle,
        name="Improvise, Adapt, Overcome",
        description="Kill enemies using a turret or vehicle-mounted weapon",
        levels=(10, 25, 150, 300, 750),
    )

    challenges[1872] = Challenge(
        position=278,
        identifier=1872,
        id_text="GD_Challenges.Vehicles.Vehicles_VehicleKillsVehicle",
        category=challenge_cat_vehicle,
        name="Road Warrior",
        description="Kill vehicles while in a vehicle",
        levels=(5, 10, 20, 40, 75),
    )

    challenges[2044] = Challenge(
        position=461,
        identifier=2044,
        id_text="GD_Challenges.Vehicles.Vehicles_KillByPancaking",
        category=challenge_cat_vehicle,
        name="Pancakes For Breakfast",
        description="Kill enemies with Stingray slams",
        levels=(1, 5, 10, 25, 50),
    )

    # Health
    challenges[1867] = Challenge(
        position=271,
        identifier=1867,
        id_text="GD_Challenges.Player.Player_PointsHealed",
        category=challenge_cat_health,
        name="Doctor Feels Good",
        description="Recover health",
        levels=(1000, 25000, 150000, 1000000, 5000000),
    )

    challenges[1815] = Challenge(
        position=201,
        identifier=1815,
        id_text="GD_Challenges.Player.Player_SecondWind",
        category=challenge_cat_health,
        name="Better You Than Me",
        description="Get Second Winds by killing an enemy",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1816] = Challenge(
        position=202,
        identifier=1816,
        id_text="GD_Challenges.Player.Player_SecondWindFromBadass",
        category=challenge_cat_health,
        name="There Can Be Only... Me",
        description="Get Second Winds by killing badass enemies",
        levels=(1, 5, 15, 30, 50),
        bonus=5,
    )

    challenges[1818] = Challenge(
        position=205,
        identifier=1818,
        id_text="GD_Challenges.Player.Player_CoopRevivesOfFriends",
        category=challenge_cat_health,
        name="Up Unt at Zem",
        description="Revive a co-op partner",
        levels=(5, 10, 50, 100, 200),
        bonus=5,
    )

    challenges[1784] = Challenge(
        position=199,
        identifier=1784,
        id_text="GD_Challenges.Player.Player_SecondWindFromFire",
        category=challenge_cat_health,
        name="The Phoenix",
        description="Get Second Winds by killing enemies with an incindiary DoT (damage over time)",
        levels=(1, 5, 15, 30, 50),
    )

    challenges[1783] = Challenge(
        position=198,
        identifier=1783,
        id_text="GD_Challenges.Player.Player_SecondWindFromCorrosive",
        category=challenge_cat_health,
        name="Soup's Up!",
        description="Get Second Winds by killing enemies with a corrosive DoT (damage over time)",
        levels=(1, 5, 15, 30, 50),
    )

    challenges[1785] = Challenge(
        position=200,
        identifier=1785,
        id_text="GD_Challenges.Player.Player_SecondWindFromShock",
        category=challenge_cat_health,
        name="Had a Bit of a Shocker",
        description="Get Second Winds by killing enemies with a shock DoT (damage over time)",
        levels=(1, 5, 15, 30, 50),
    )

    challenges[2057] = Challenge(
        position=473,
        identifier=2057,
        id_text="GD_Challenges.Player.Player_SecondWindFromShatter",
        category=challenge_cat_health,
        name="Rollin' the Ice",
        description="Get Second Winds by shattering frozen enemies",
        levels=(1, 5, 15, 30, 50),
    )

    # Grenades
    challenges[1589] = Challenge(
        position=31,
        identifier=1589,
        id_text="GD_Challenges.Grenades.Grenade_Kills",
        category=challenge_cat_grenades,
        name="Home Nade Cookin'",
        description="Kill enemies with grenades",
        levels=(10, 25, 150, 300, 750),
        bonus=3,
    )

    challenges[1836] = Challenge(
        position=239,
        identifier=1836,
        id_text="GD_Challenges.Grenades.Grenade_KillsSingularityType",
        category=challenge_cat_grenades,
        name="See Ya on the Other Side",
        description="Kill enemies with Singularity grenades",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1835] = Challenge(
        position=238,
        identifier=1835,
        id_text="GD_Challenges.Grenades.Grenade_KillsMirvType",
        category=challenge_cat_grenades,
        name="Big MIRV",
        description="Kill enemies with MIRV grenades",
        levels=(10, 25, 75, 150, 300),
        bonus=3,
    )

    challenges[1833] = Challenge(
        position=236,
        identifier=1833,
        id_text="GD_Challenges.Grenades.Grenade_KillsAoEoTType",
        category=challenge_cat_grenades,
        name="Sprayowee",
        description="Kill enemies with Area-of-Effect grenades",
        levels=(25, 50, 125, 250, 500),
    )

    challenges[1834] = Challenge(
        position=237,
        identifier=1834,
        id_text="GD_Challenges.Grenades.Grenade_KillsBouncing",
        category=challenge_cat_grenades,
        name="Betty Boom",
        description="Kill enemies with Bouncing Betty grenades",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1868] = Challenge(
        position=240,
        identifier=1868,
        id_text="GD_Challenges.Grenades.Grenade_KillsTransfusionType",
        category=challenge_cat_grenades,
        name="Pass the Chianti",
        description="Kill enemies with Transfusion grenades",
        levels=(10, 25, 75, 150, 300),
    )

    # Shields
    challenges[1839] = Challenge(
        position=244,
        identifier=1839,
        id_text="GD_Challenges.Shields.Shields_KillsNova",
        category=challenge_cat_shields,
        name="Nova Say Die",
        description="Kill enemies with a Nova shield burst",
        levels=(5, 10, 50, 100, 200),
        bonus=3,
    )

    challenges[1840] = Challenge(
        position=245,
        identifier=1840,
        id_text="GD_Challenges.Shields.Shields_KillsRoid",
        category=challenge_cat_shields,
        name="Wet Work",
        description="Kill enemies while buffed by a Maylay shield",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[1841] = Challenge(
        position=246,
        identifier=1841,
        id_text="GD_Challenges.Shields.Shields_KillsSpikes",
        category=challenge_cat_shields,
        name="That'll Learn Ya",
        description="Kill enemies with reflected damage from a Spike shield",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[1842] = Challenge(
        position=247,
        identifier=1842,
        id_text="GD_Challenges.Shields.Shields_KillsImpact",
        category=challenge_cat_shields,
        name="Amplitude Killulation",
        description="Kill enemies while buffed by an Amplify shield",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[1880] = Challenge(
        position=223,
        identifier=1880,
        id_text="GD_Challenges.Shields.Shields_AbsorbAmmo",
        category=challenge_cat_shields,
        name="Ammo Eater",
        description="Absorb enemy ammo with an Absorption shield",
        levels=(20, 75, 250, 600, 1000),
        bonus=5,
    )

    # Rocket Launchers
    challenges[1712] = Challenge(
        position=32,
        identifier=1712,
        id_text="GD_Challenges.Weapons.Launcher_Kills",
        category=challenge_cat_rockets,
        name="Get a Rocket up Ya",
        description="Kill enemies with rocket launchers",
        levels=(10, 50, 100, 250, 500),
        bonus=3,
    )

    challenges[1778] = Challenge(
        position=193,
        identifier=1778,
        id_text="GD_Challenges.Weapons.Launcher_SecondWinds",
        category=challenge_cat_rockets,
        name="Magic Missile",
        description="Get Second Winds with rocket launchers",
        levels=(2, 5, 15, 30, 50),
    )

    challenges[1820] = Challenge(
        position=225,
        identifier=1820,
        id_text="GD_Challenges.Weapons.Launcher_KillsSplashDamage",
        category=challenge_cat_rockets,
        name="Collateral Damage",
        description="Kill enemies with rocket launcher splash damage",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[1819] = Challenge(
        position=224,
        identifier=1819,
        id_text="GD_Challenges.Weapons.Launcher_KillsDirectHit",
        category=challenge_cat_rockets,
        name="Missile Magnet",
        description="Kill enemies with direct hits from rocket launchers",
        levels=(5, 10, 50, 100, 200),
        bonus=5,
    )

    challenges[1821] = Challenge(
        position=54,
        identifier=1821,
        id_text="GD_Challenges.Weapons.Launcher_KillsFullShieldEnemy",
        category=challenge_cat_rockets,
        name="Punker Buster",
        description="Kill shielded enemies with one rocket each",
        levels=(5, 15, 35, 75, 125),
    )

    challenges[1758] = Challenge(
        position=52,
        identifier=1758,
        id_text="GD_Challenges.Weapons.Launcher_KillsLongRange",
        category=challenge_cat_rockets,
        name="Hand of God",
        description="Kill enemies from long range with rocket launchers",
        levels=(25, 100, 400, 1000, 2000),
    )

    # Sniper Rifles
    challenges[1586] = Challenge(
        position=28,
        identifier=1586,
        id_text="GD_Challenges.Weapons.SniperRifle_Kills",
        category=challenge_cat_sniper,
        name="Sharp Shooter",
        description="Kill enemies with sniper rifles",
        levels=(20, 100, 500, 2500, 5000),
        bonus=3,
    )

    challenges[1616] = Challenge(
        position=179,
        identifier=1616,
        id_text="GD_Challenges.Weapons.Sniper_CriticalHits",
        category=challenge_cat_sniper,
        name="Melon Splitter",
        description="Get critical hits with sniper rifles",
        levels=(25, 100, 400, 1000, 2000),
    )

    challenges[1774] = Challenge(
        position=189,
        identifier=1774,
        id_text="GD_Challenges.Weapons.Sniper_SecondWinds",
        category=challenge_cat_sniper,
        name="Windage Adjustment",
        description="Get Second Winds with sniper rifles",
        levels=(2, 5, 15, 30, 50),
    )

    challenges[1794] = Challenge(
        position=59,
        identifier=1794,
        id_text="GD_Challenges.Weapons.Sniper_CriticalHitKills",
        category=challenge_cat_sniper,
        name="Critical Reception",
        description="Kill enemies with critical hits using sniper rifles",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1748] = Challenge(
        position=47,
        identifier=1748,
        id_text="GD_Challenges.Weapons.SniperRifle_KillsFromHip",
        category=challenge_cat_sniper,
        name="Ol' Skool",
        description="Kill enemies with sniper rifles without using the scope/ironsights",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[1831] = Challenge(
        position=234,
        identifier=1831,
        id_text="GD_Challenges.Weapons.SniperRifle_KillsUnaware",
        category=challenge_cat_sniper,
        name="Clean and Simple",
        description="Kill unaware enemies with sniper rifles",
        levels=(5, 10, 50, 100, 200),
    )

    challenges[1822] = Challenge(
        position=55,
        identifier=1822,
        id_text="GD_Challenges.Weapons.SniperRifle_KillsFullShieldEnemy",
        category=challenge_cat_sniper,
        name="Penetrating Wound",
        description="Kill shielded enemies with one shot using sniper rifles",
        levels=(5, 15, 35, 75, 125),
        bonus=5,
    )

    # Assault Rifles
    challenges[1587] = Challenge(
        position=29,
        identifier=1587,
        id_text="GD_Challenges.Weapons.AssaultRifle_Kills",
        category=challenge_cat_ar,
        name="Assault With a Deadly Weapon",
        description="Kill enemies with assault rifles",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )

    challenges[1617] = Challenge(
        position=180,
        identifier=1617,
        id_text="GD_Challenges.Weapons.AssaultRifle_CriticalHits",
        category=challenge_cat_ar,
        name="Aim to Please",
        description="Get critical hits with assault rifles",
        levels=(25, 100, 400, 1000, 2000),
    )

    challenges[1775] = Challenge(
        position=190,
        identifier=1775,
        id_text="GD_Challenges.Weapons.AssaultRifle_SecondWinds",
        category=challenge_cat_ar,
        name="Assaulty Dog",
        description="Get Second Winds with assault rifles",
        levels=(5, 15, 30, 50, 75),
    )

    challenges[1795] = Challenge(
        position=60,
        identifier=1795,
        id_text="GD_Challenges.Weapons.AssaultRifle_CriticalHitKills",
        category=challenge_cat_ar,
        name="Hot Lead Injection",
        description="Kill enemies with critical hits using assault rifles",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1747] = Challenge(
        position=46,
        identifier=1747,
        id_text="GD_Challenges.Weapons.AssaultRifle_KillsCrouched",
        category=challenge_cat_ar,
        name="Crouch Potato",
        description="Kill enemies with assault rifles while crouched",
        levels=(25, 75, 400, 1600, 3200),
        bonus=5,
    )

    # Laser
    challenges[1984] = Challenge(
        position=401,
        identifier=1984,
        id_text="GD_Challenges.Weapons.Laser_CriticalHitKills",
        category=challenge_cat_laser,
        name="Light 'em Up",
        description="Kill enemies with critical hits using laser weapons",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1982] = Challenge(
        position=399,
        identifier=1982,
        id_text="GD_Challenges.Weapons.Laser_CriticalHits",
        category=challenge_cat_laser,
        name="Aggressive Lasik",
        description="Get critical hits with lasers",
        levels=(25, 100, 400, 1000, 2000),
    )

    challenges[2045] = Challenge(
        position=462,
        identifier=2045,
        id_text="GD_Challenges.Weapons.Laser_FlyingKills",
        category=challenge_cat_laser,
        name="Battle Star",
        description="Kill flying enemies with laser weapons while airborne",
        levels=(10, 25, 150, 300, 750),
        bonus=5,
    )

    challenges[1981] = Challenge(
        position=398,
        identifier=1981,
        id_text="GD_Challenges.Weapons.Laser_Kills",
        category=challenge_cat_laser,
        name="Pew Pew",
        description="Kill enemies with laser weapons",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )

    challenges[1983] = Challenge(
        position=400,
        identifier=1983,
        id_text="GD_Challenges.Weapons.Laser_SecondWinds",
        category=challenge_cat_laser,
        name="I See the Light",
        description="Get Second Winds with laser weapons",
        levels=(2, 5, 15, 30, 50),
    )

    # SMGs
    challenges[1585] = Challenge(
        position=27,
        identifier=1585,
        id_text="GD_Challenges.Weapons.SMG_Kills",
        category=challenge_cat_smg,
        name="Nice Spray Job",
        description="Kill enemies with SMGs",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )

    challenges[1615] = Challenge(
        position=178,
        identifier=1615,
        id_text="GD_Challenges.Weapons.SMG_CriticalHits",
        category=challenge_cat_smg,
        name="Bring the Pain",
        description="Get critical hits with SMGs",
        levels=(25, 100, 400, 1000, 2000),
    )

    challenges[1793] = Challenge(
        position=58,
        identifier=1793,
        id_text="GD_Challenges.Weapons.SMG_CriticalHitKills",
        category=challenge_cat_smg,
        name="Dinky Death Dealer",
        description="Kill enemies with critical hits using SMGs",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1773] = Challenge(
        position=188,
        identifier=1773,
        id_text="GD_Challenges.Weapons.SMG_SecondWinds",
        category=challenge_cat_smg,
        name="And Stay Down!",
        description="Get Second Winds with SMGs",
        levels=(2, 5, 15, 30, 50),
    )

    # Shotguns
    challenges[1584] = Challenge(
        position=26,
        identifier=1584,
        id_text="GD_Challenges.Weapons.Shotgun_Kills",
        category=challenge_cat_shotgun,
        name="Boomstick Boogie",
        description="Kill enemies with shotguns",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )

    challenges[1614] = Challenge(
        position=177,
        identifier=1614,
        id_text="GD_Challenges.Weapons.Shotgun_CriticalHits",
        category=challenge_cat_shotgun,
        name="Hello Uncle Buckshot",
        description="Get critical hits with shotguns",
        levels=(50, 250, 1000, 2500, 5000),
    )

    challenges[1772] = Challenge(
        position=187,
        identifier=1772,
        id_text="GD_Challenges.Weapons.Shotgun_SecondWinds",
        category=challenge_cat_shotgun,
        name="Shotgunning the Breeze",
        description="Get Second Winds with shotguns",
        levels=(2, 5, 15, 30, 50),
    )

    challenges[1756] = Challenge(
        position=50,
        identifier=1756,
        id_text="GD_Challenges.Weapons.Shotgun_KillsPointBlank",
        category=challenge_cat_shotgun,
        name="Take It All!",
        description="Kill enemies from point-blank range with shotguns",
        levels=(10, 25, 150, 300, 750),
    )

    challenges[1757] = Challenge(
        position=51,
        identifier=1757,
        id_text="GD_Challenges.Weapons.Shotgun_KillsLongRange",
        category=challenge_cat_shotgun,
        name="Over Achiever",
        description="Kill enemies from long range with shotguns",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1792] = Challenge(
        position=57,
        identifier=1792,
        id_text="GD_Challenges.Weapons.Shotgun_CriticalHitKills",
        category=challenge_cat_shotgun,
        name="Shotty Workmanship",
        description="Kill enemies with critical hits using shotguns",
        levels=(10, 50, 100, 250, 500),
    )

    # Pistols
    challenges[1583] = Challenge(
        position=25,
        identifier=1583,
        id_text="GD_Challenges.Weapons.Pistol_Kills",
        category=challenge_cat_pistol,
        name="Trigger Happy",
        description="Kill enemies with pistols",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )

    challenges[1613] = Challenge(
        position=176,
        identifier=1613,
        id_text="GD_Challenges.Weapons.Pistol_CriticalHits",
        category=challenge_cat_pistol,
        name="Pistoleer",
        description="Get critical hits with pistols",
        levels=(25, 100, 400, 1000, 2000),
    )

    challenges[1771] = Challenge(
        position=186,
        identifier=1771,
        id_text="GD_Challenges.Weapons.Pistol_SecondWinds",
        category=challenge_cat_pistol,
        name="Pistol Whipped",
        description="Get Second Winds with pistols",
        levels=(2, 5, 15, 30, 50),
    )

    challenges[1791] = Challenge(
        position=56,
        identifier=1791,
        id_text="GD_Challenges.Weapons.Pistol_CriticalHitKills",
        category=challenge_cat_pistol,
        name="Magnum Maestro",
        description="Kill enemies with critical hits using pistols",
        levels=(10, 25, 75, 150, 300),
    )

    challenges[1750] = Challenge(
        position=49,
        identifier=1750,
        id_text="GD_Challenges.Weapons.Pistol_KillsQuickshot",
        category=challenge_cat_pistol,
        name="Gunslinger",
        description="Kill enemies shortly after aiming down the sights with a pistol",
        levels=(10, 25, 150, 300, 750),
        bonus=5,
    )

    # Melee
    challenges[1600] = Challenge(
        position=75,
        identifier=1600,
        id_text="GD_Challenges.Melee.Melee_Kills",
        category=challenge_cat_melee,
        name="Martial Marhsal",
        description="Kill enemies with melee attacks",
        levels=(25, 100, 400, 1000, 2000),
        bonus=3,
    )

    challenges[1843] = Challenge(
        position=248,
        identifier=1843,
        id_text="GD_Challenges.Melee.Melee_KillsBladed",
        category=challenge_cat_melee,
        name="Captain Cutty",
        description="Kill enemies with melee attacks using bladed guns",
        levels=(20, 75, 250, 600, 1000),
    )

    # General Combat
    challenges[1571] = Challenge(
        position=0,
        identifier=1571,
        id_text="GD_Challenges.GeneralCombat.General_RoundsFired",
        category=challenge_cat_combat,
        name="Projectile Proliferation",
        description="Fire a lot of rounds",
        levels=(5000, 10000, 25000, 50000, 75000),
        bonus=5,
    )

    challenges[1652] = Challenge(
        position=90,
        identifier=1652,
        id_text="GD_Challenges.GeneralCombat.Player_KillsWithActionSkill",
        category=challenge_cat_combat,
        name="Action Hero",
        description="Kill enemies while using your Action Skill",
        levels=(20, 75, 250, 750, 1500),
    )

    challenges[1866] = Challenge(
        position=270,
        identifier=1866,
        id_text="GD_Challenges.GeneralCombat.Kills_AtNight",
        category=challenge_cat_combat,
        name="Dark Sider",
        description="Kill enemies at night",
        levels=(25, 100, 500, 1000, 1500),
    )

    challenges[1865] = Challenge(
        position=269,
        identifier=1865,
        id_text="GD_Challenges.GeneralCombat.Kills_AtDay",
        category=challenge_cat_combat,
        name="Day of the Dead",
        description="Kill enemies during the day",
        levels=(250, 1000, 2500, 5000, 7500),
    )

    challenges[1858] = Challenge(
        position=262,
        identifier=1858,
        id_text="GD_Challenges.GeneralCombat.Tediore_KillWithReload",
        category=challenge_cat_combat,
        name="Throw Me the Money!",
        description="Kill enemies with Tediore reloads",
        levels=(5, 10, 25, 75, 150),
        bonus=5,
    )

    challenges[1859] = Challenge(
        position=263,
        identifier=1859,
        id_text="GD_Challenges.GeneralCombat.Tediore_DamageFromReloads",
        category=challenge_cat_combat,
        name="One Man's Trash",
        description="Deal damage with Tediore reloads",
        levels=(5000, 20000, 100000, 500000, 1000000),
    )

    challenges[1862] = Challenge(
        position=266,
        identifier=1862,
        id_text="GD_Challenges.GeneralCombat.Barrels_KillEnemies",
        category=challenge_cat_combat,
        name="Barrel of Laughs",
        description="Kill enemies with stationary barrels",
        levels=(10, 25, 50, 100, 200),
        bonus=3,
    )

    challenges[1596] = Challenge(
        position=44,
        identifier=1596,
        id_text="GD_Challenges.GeneralCombat.Kills_FromCrits",
        category=challenge_cat_combat,
        name="Executioner",
        description="Kill enemies with critical hits",
        levels=(20, 100, 500, 1000, 1500),
    )

    challenges[2046] = Challenge(
        position=463,
        identifier=2046,
        id_text="GD_Challenges.GeneralCombat.Break_Masks",
        category=challenge_cat_combat,
        name="Having Trouble Breathing?",
        description="Shatter enemy oxygen masks",
        levels=(25, 100, 250, 500, 1000),
    )

    challenges[2047] = Challenge(
        position=464,
        identifier=2047,
        id_text="GD_Challenges.GeneralCombat.Kills_Asphyxiation",
        category=challenge_cat_combat,
        name="Last Gasp",
        description="Kill enemies by asphyxiation",
        levels=(10, 25, 150, 300, 750),
    )

    challenges[2050] = Challenge(
        position=466,
        identifier=2050,
        id_text="GD_Challenges.GeneralCombat.Shatter_With_Falling",
        category=challenge_cat_combat,
        name="Comet Crash",
        description="Shatter frozen enemies with falling damage",
        levels=(5, 10, 50, 100, 200),
        bonus=5,
    )

    challenges[2049] = Challenge(
        position=465,
        identifier=2049,
        id_text="GD_Challenges.GeneralCombat.Shatter_With_Weapons",
        category=challenge_cat_combat,
        name="Ice to Meet You",
        description="Shatter frozen enemies with weapons",
        levels=(20, 75, 250, 600, 1000),
    )

    # Miscellaneous
    challenges[1609] = Challenge(
        position=105,
        identifier=1609,
        id_text="GD_Challenges.Dueling.DuelsWon_HatersGonnaHate",
        category=challenge_cat_misc,
        name="The Duelist",
        description="Win duels",
        levels=(1, 5, 15, 30, 50),
    )

    challenges[1754] = Challenge(
        position=212,
        identifier=1754,
        id_text="GD_Challenges.Miscellaneous.Missions_SideMissionsCompleted",
        category=challenge_cat_misc,
        name="Little on the Side",
        description="Complete side missions",
        levels=(10, 25, 50, 75, 125),
    )

    challenges[1753] = Challenge(
        position=211,
        identifier=1753,
        id_text="GD_Challenges.Miscellaneous.Missions_OptionalObjectivesCompleted",
        category=challenge_cat_misc,
        name="OC/DC",
        description="Complete optional mission objectives",
        levels=(5, 10, 15, 20, 30),
    )

    challenges[1648] = Challenge(
        position=174,
        identifier=1648,
        id_text="GD_Challenges.Miscellaneous.Misc_CompleteChallenges",
        category=challenge_cat_misc,
        name="We Have a Contender",
        description="Complete many, many challenges",
        levels=(5, 25, 50, 100, 200),
    )

    return challenges
