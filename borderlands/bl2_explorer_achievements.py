import dataclasses
from typing import Final, Dict, List


@dataclasses.dataclass(frozen=True)
class ExplorerAchievementInfo:
    name: str
    explanation: str
    guide_url: str
    code_to_name_map: Dict[str, str]


_BL2_EXPLORER_ACHIEVEMENTS: Final = (
    ExplorerAchievementInfo(
        name='World Traveler',
        explanation='Discovered all named locations',
        guide_url='https://www.playstationtrophies.org/forum/topic/161466-complete-world-map-world-traveler-trophy/',
        code_to_name_map={
            'Ash_P': 'Eridium Blight',
            'BanditSlaughter_P': 'Fink\'s Slaughterhouse',
            'Boss_Cliffs_P': 'The Bunker',
            'Boss_Volcano_P': 'Vault of the Warrior',
            'Cove_P': 'Southern Shelf - Bay',
            'CraterLake_P': 'Sawtooth Cauldron',
            'CreatureSlaughter_P': 'Natural Selection Annex',
            'FinalBossAscent_P': 'Hero\'s Pass',
            'Fridge_P': 'The Fridge',
            'Frost_P': 'Three Horns Valley',
            'Fyrestone_P': 'Arid Nexus - Boneyard',
            'Glacial_P': 'Claptrap\'s Place / Windshear Waste',
            'Grass_Cliffs_P': 'Thousand Cuts',
            'Grass_Lynchwood_P': 'Lynchwood',
            'Grass_P': 'The Highlands',
            'HypInterlude_P': 'Friendship Gulag',
            'HyperionCity_P': 'Opportunity',
            'Ice_P': 'Three Horns Divide',
            'Interlude_P': 'The Dust',
            'Luckys_P': 'The Holy Spirits',
            'Outwash_P': 'The Highlands - Outwash',
            'PandoraPark_P': 'Wildlife Exploitation Preserve',
            'RobotSlaughter_P': 'Ore Chasm',
            'Sanctuary_Hole_P': 'Sanctuary Hole',
            'Sanctuary_P': 'Sanctuary',
            'SouthernShelf_P': 'Southern Shelf',
            'SouthpawFactory_P': 'Southpaw Steam & Power',
            'Stockade_P': 'Arid Nexus - Badlands',
            'ThresherRaid_P': 'Terramorphous Peak',
            'TundraTrain_P': 'End of the Line',
            'VOGChamber_P': 'Control Core Angel',
            'caverns_p': 'Caustic Caverns',
            'dam_p': 'Bloodshot Stronghold',
            'damtop_p': 'Bloodshot Ramparts',
            'icecanyon_p': 'Frostburn Canyon',
            'tundraexpress_p': 'Tundra Express',
        },
    ),
    ExplorerAchievementInfo(
        name='Arctic Explorer',
        explanation='Discovered all named locations in Three Horns, Tundra Express, and Frostburn Canyon',
        guide_url='https://www.trueachievements.com/a167557/arctic-explorer-achievement',
        code_to_name_map={
            'Frost_P': 'Three Horns Valley',
            'Ice_P': 'Three Horns Divide',
            'icecanyon_p': 'Frostburn Canyon',
            'tundraexpress_p': 'Tundra Express',
        },
    ),
    ExplorerAchievementInfo(
        name='Urban Explorer',
        explanation='Discovered all named locations in Sanctuary, Opportunity, and Lynchwood',
        guide_url='https://www.trueachievements.com/a167558/urban-explorer-achievement',
        code_to_name_map={
            'Grass_Lynchwood_P': 'Lynchwood',
            'HyperionCity_P': 'Opportunity',
            'Sanctuary_P': 'Sanctuary',
        },
    ),
    ExplorerAchievementInfo(
        name='Highlands Explorer',
        explanation='Discovered all named locations in The Highlands, Thousand Cuts and Wildlife Exploitation Preserve',
        guide_url='https://www.trueachievements.com/a167559/highlands-explorer-achievement',
        code_to_name_map={
            'Grass_Cliffs_P': 'Thousand Cuts',
            'Grass_P': 'The Highlands',
            'Outwash_P': 'The Highlands - Outwash',
            'PandoraPark_P': 'Wildlife Exploitation Preserve',
        },
    ),
    ExplorerAchievementInfo(
        name='Blight Explorer',
        explanation='Discovered all named locations in Eridium Blight, Arid Nexus, and Sawtooth Cauldron',
        guide_url='https://www.trueachievements.com/a167560/blight-explorer-achievement',
        code_to_name_map={
            'Ash_P': 'Eridium Blight',
            'CraterLake_P': 'Sawtooth Cauldron',
            'Fyrestone_P': 'Arid Nexus - Boneyard',
            'Stockade_P': 'Arid Nexus - Badlands',
        },
    ),
    ExplorerAchievementInfo(
        name='Gadabout',
        explanation='Discovered all named locations in Oasis and the surrounding Pirate\'s Booty areas',
        guide_url='https://www.trueachievements.com/a170077/gadabout-achievement',
        code_to_name_map={
            'Orchid_Caves_P': 'Hayter\'s Folly',
            'Orchid_OasisTown_P': 'Oasis',
            'Orchid_Refinery_P': 'Washburne Refinery',
            'Orchid_SaltFlats_P': 'Wurmwater',
            'Orchid_ShipGraveyard_P': 'The Rustyards',
            'Orchid_Spire_P': 'Magnys Lighthouse',
            'Orchid_WormBelly_P': 'The Leviathan\'s Lair',
        },
    ),
    ExplorerAchievementInfo(
        name='Been There',
        explanation='Discovered all named locations in Hammerlock\'s Hunt',
        guide_url='https://www.trueachievements.com/a199051/been-there-achievement',
        code_to_name_map={
            'Sage_Cliffs_P': 'Candlerakk\'s Crag',
            'Sage_HyperionShip_P': 'H.S.S. Terminus',
            'Sage_PowerStation_P': 'Ardorton Station',
            'Sage_RockForest_P': 'Scylla\'s Grove',
            'Sage_Underground_P': 'Hunter\'s Grotto',
        },
    ),
)

_NOT_EXPLORER_ACHIEVEMENTS_MAP: Final = {
    'BackBurner_P': 'The Backburner',
    'CastleExterior_P': 'Hatred\'s Shadow',
    'CastleKeep_P': 'Dragon Keep',
    'Dark_Forest_P': 'The Forest',
    'Dead_Forest_P': 'Immortal Woods',
    'Distillery_P': 'Rotgut Distillery',
    'Docks_P': 'Unassuming Docks',
    'DungeonRaid_P': 'The Winged Storm',
    'Dungeon_P': 'Lair of Infinite Agony',
    'Easter_P': 'Wam Bam Island',
    'GaiusSanctuary_P': 'Paradise Sanctum',
    'Helios_P': 'Helios Fallen',
    'Hunger_P': 'Gluttony Gulch',
    'Iris_DL1_P': 'Arena',
    'Iris_DL1_TAS_P': 'Arena',
    'Iris_DL2_Interior_P': 'Pyro Pete\'s Bar',
    'Iris_DL2_P': 'The Beatdown',
    'Iris_DL3_P': 'Forge',
    'Iris_Hub2_P': 'Southern Raceway',
    'Iris_Hub_P': 'Badass Crater of Badassitude',
    'Iris_Moxxi_P': 'Badass Crater Bar',
    'Mines_P': 'Mines of Avarice',
    'OldDust_P': 'Dahl Abandon',
    'Pumpkin_Patch_P': 'Hallowed Hollow',
    'ResearchCenter_P': 'Mt. Scarab Research Center',
    'Sage_Cliffs_P': 'Candlerakk\'s Crag',
    'SanctIntro_P': 'Fight for Sanctuary',
    'SandwormLair_P': 'Writhing Deep',
    'Sandworm_P': 'The Burrows',
    'TempleSlaughter_P': 'Murderlin\'s Temple',
    'TestingZone_P': 'The Raid on Digistruct Peak',
    'Village_P': 'Flamerock Refuge',
    'Xmas_P': 'Marcus\'s Mercenary Shop',
}


def report_one_explorer_achievement(*, fully_explored_maps: List[str], info: ExplorerAchievementInfo) -> List[str]:
    result = []
    all_maps = set(info.code_to_name_map.keys())
    incomplete_maps = all_maps - set(fully_explored_maps)
    complete_maps = all_maps - incomplete_maps
    if incomplete_maps:
        result.append(f'{info.name} - Partially ({len(complete_maps)}/{len(all_maps)})')
        result.append(f'More details: {info.guide_url}')
        result.append(f'Incomplete maps ({len(incomplete_maps)}):')
        pairs = [(info.code_to_name_map[k], k) for k in incomplete_maps]
        pairs.sort()
        for name, code in pairs:
            result.append(f'  {name}')
        result.append('')
    else:
        result.append(f'{info.name} - Complete')

    return result


def create_explorer_achievements_report(fully_explored_maps: List[str]) -> List[str]:
    result = []
    for info in _BL2_EXPLORER_ACHIEVEMENTS:
        result.extend(report_one_explorer_achievement(fully_explored_maps=fully_explored_maps, info=info))
    result.append('')
    return result
