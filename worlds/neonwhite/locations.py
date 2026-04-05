# Locations are specific points that you would obtain an item at.
from BaseClasses import Location


class NWLocation(Location):
    game: str = "Neon White"


neon_white_levels_normal = [
    "Movement",
    "Pummel",
    "Gunner",
    "Cascade",
    "Elevate",
    "Bounce",
    "Purify",
    "Climb",
    "Fasttrack",
    "Glass Port",
    "Take Flight",
    "Godspeed",
    "Dasher",
    "Thrasher",
    "Outstretched",
    "Smackdown",
    "Catwalk",
    "Fastlane",
    "Distinguish",
    "Dancer",
    "Guardian",
    "Stomp",
    "Jumper",
    "Dash Tower",
    "Descent",
    "Driller",
    "Canals",
    "Sprint",
    "Mountain",
    "Superkinetic",
    "Arrival",
    "Forgotten City",
    "Fireball",
    "Ringer",
    "Cleaner",
    "Warehouse",
    "Boom",
    "Streets",
    "Steps",
    "Demolition",
    "Arcs",
    "Apartment",
    "Hanging Gardens",
    "Tangled",
    "Waterworks",
    "Killswitch",
    "Falling",
    "Shocker",
    "Bouquet",
    "Prepare",
    "Triptrack",
    "Race",
    "Bubble",
    "Shield",
    "Overlook",
    "Pop",
    "Minefield",
    "Mimic",
    "Trigger",
    "Greenhouse",
    "Sweep",
    "Fuse",
    "Heaven's Edge",
    "Zipline",
    "Swing",
    "Chute",
    "Crash",
    "Ascent",
    "Straightaway",
    "Firecracker",
    "Streak",
    "Mirror",
    "Escalation",
    "Bolt",
    "Godstreak",
    "Plunge",
    "Mayhem",
    "Barrage",
    "Estate",
    "Trapwire",
    "Ricochet",
    "Fortress",
    "Holy Ground",
    "Spree",
    "Breakthrough",
    "Glide",
    "Closer",
    "Hike",
    "Switch",
    "Access",
    "Congregation",
    "Sequence",
    "Marathon",
]

neon_white_levels_giftless = [
    "The Clocktower",
    "The Third Temple",
    "Sacrifice",
    "Absolution"
]

neon_white_levels_sidequests = [  # No gifts either
    "Elevate Traversal I",
    "Elevate Traversal II",
    "Purify Traversal",
    "Godspeed Traversal",
    "Stomp Traversal",
    "Fireball Traversal",
    "Dominion Traversal",
    "Book of Life Traversal",
    "Doghouse",
    "Choker",
    "Chain",
    "Hellevator",
    "Razor",
    "All Seeing Eye",
    "Resident Saw I",
    "Resident Saw II",
    "Sunset Flip Powerbomb",
    "Balloon Mountain",
    "Climbing Gym",
    "Fisherman Suplex",
    "STF",
    "Arena",
    "Attitude Adjustment",
    "Rocket"
]

neon_white_levels_medals = [
    "Bronze",
    "Silver",
    "Gold",
    "Ace",
    "Dev"
]

# fmt: off
neon_white_level_name_internal = {
    "Movement": "TUT_MOVEMENT",
    "Pummel": "TUT_SHOOTINGRANGE",
    "Gunner": "SLUGGER",
    "Cascade": "TUT_FROG",
    "Elevate": "TUT_JUMP",
    "Bounce": "GRID_TUT_BALLOON",
    "Purify": "TUT_BOMB2",
    "Climb": "TUT_BOMBJUMP",
    "Fasttrack": "TUT_FASTTRACK",
    "Glass Port": "GRID_PORT",
    "Take Flight": "GRID_PAGODA",
    "Godspeed": "TUT_RIFLE",
    "Dasher": "TUT_RIFLEJOCK",
    "Thrasher": "TUT_DASHENEMY",
    "Outstretched": "GRID_JUMPDASH",
    "Smackdown": "GRID_SMACKDOWN",
    "Catwalk": "GRID_MEATY_BALLOONS",
    "Fastlane": "GRID_FAST_BALLOON",
    "Distinguish": "GRID_DRAGON2",
    "Dancer": "GRID_DASHDANCE",
    "Guardian": "TUT_GUARDIAN",
    "Stomp": "TUT_UZI",
    "Jumper": "TUT_JUMPER",
    "Dash Tower": "TUT_BOMB",
    "Descent": "GRID_DESCEND",
    "Driller": "GRID_STAMPEROUT",
    "Canals": "GRID_CRUISE",
    "Sprint": "GRID_SPRINT",
    "Mountain": "GRID_MOUNTAIN",
    "Superkinetic": "GRID_SUPERKINETIC",
    "Arrival": "GRID_ARRIVAL",
    "Forgotten City": "FLOATING",
    "The Clocktower": "GRID_BOSS_YELLOW",
    "Fireball": "GRID_HOPHOP",
    "Ringer": "GRID_RINGER_TUTORIAL",
    "Cleaner": "GRID_RINGER_EXPLORATION",
    "Warehouse": "GRID_HOPSCOTCH",
    "Boom": "GRID_BOOM",
    "Streets": "GRID_SNAKE_IN_MY_BOOT",
    "Steps": "GRID_FLOCK",
    "Demolition": "GRID_BOMBS_AHOY",
    "Arcs": "GRID_ARCS",
    "Apartment": "GRID_APARTMENT",
    "Hanging Gardens": "TUT_TRIPWIRE",
    "Tangled": "GRID_TANGLED",
    "Waterworks": "GRID_HUNT",
    "Killswitch": "GRID_CANNONS",
    "Falling": "GRID_FALLING",
    "Shocker": "TUT_SHOCKER2",
    "Bouquet": "TUT_SHOCKER",
    "Prepare": "GRID_PREPARE",
    "Triptrack": "GRID_TRIPMAZE",
    "Race": "GRID_RACE",
    "Bubble": "TUT_FORCEFIELD2",
    "Shield": "GRID_SHIELD",
    "Overlook": "SA L VAGE2",
    "Pop": "GRID_VERTICAL",
    "Minefield": "GRID_MINEFIELD",
    "Mimic": "TUT_MIMIC",
    "Trigger": "GRID_MIMICPOP",
    "Greenhouse": "GRID_SWARM",
    "Sweep": "GRID_SWITCH",
    "Fuse": "GRID_TRAPS2",
    "Heaven's Edge": "TUT_ROCKETJUMP",
    "Zipline": "TUT_ZIPLINE",
    "Swing": "GRID_CLIMBANG",
    "Chute": "GRID_ROCKETUZI",
    "Crash": "GRID_CRASHLAND",
    "Ascent": "GRID_ESCALATE",
    "Straightaway": "GRID_SPIDERCLAUS",
    "Firecracker": "GRID_FIRECRACKER_2",
    "Streak": "GRID_SPIDERMAN",
    "Mirror": "GRID_DESTRUCTION",
    "Escalation": "GRID_HEAT",
    "Bolt": "GRID_BOLT",
    "Godstreak": "GRID_PON",
    "Plunge": "GRID_CHARGE",
    "Mayhem": "GRID_MIMICFINALE",
    "Barrage": "GRID_BARRAGE",
    "Estate": "GRID_1GUN",
    "Trapwire": "GRID_HECK",
    "Ricochet": "GRID_ANTFARM",
    "Fortress": "GRID_FORTRESS",
    "Holy Ground": "GRID_GODTEMPLE_ENTRY",
    "The Third Temple": "GRID_BOSS_GODSDEATHTEMPLE",
    "Spree": "GRID_EXTERMINATOR",
    "Breakthrough": "GRID_FEVER",
    "Glide": "GRID_SKIPSLIDE",
    "Closer": "GRID_CLOSER",
    "Hike": "GRID_HIKE",
    "Switch": "GRID_SKIP",
    "Access": "GRID_CEILING",
    "Congregation": "GRID_BOOP",
    "Sequence": "GRID_TRIPRAP",
    "Marathon": "GRID_ZIPRAP",
    "Sacrifice": "TUT_ORIGIN",
    "Absolution": "GRID_BOSS_RAPTURE",
    "Elevate Traversal I": "SIDEQUEST_OBSTACLE_PISTOL",
    "Elevate Traversal II": "SIDEQUEST_OBSTACLE_PISTOL_SHOOT",
    "Purify Traversal": "SIDEQUEST_OBSTACLE_MACHINEGUN",
    "Godspeed Traversal": "SIDEQUEST_OBSTACLE_RIFLE_2",
    "Stomp Traversal": "SIDEQUEST_OBSTACLE_UZI2",
    "Fireball Traversal": "SIDEQUEST_OBSTACLE_SHOTGUN",
    "Dominion Traversal": "SIDEQUEST_OBSTACLE_ROCKETLAUNCHER",
    "Book of Life Traversal": "SIDEQUEST_RAPTURE_QUEST",
    "Doghouse": "SIDEQUEST_DODGER",
    "Choker": "GRID_GLASSPATH",
    "Chain": "GRID_GLASSPATH2",
    "Hellevator": "GRID_HELLVATOR",
    "Razor": "GRID_GLASSPATH3",
    "All Seeing Eye": "SIDEQUEST_ALL_SEEING_EYE",
    "Resident Saw I": "SIDEQUEST_RESIDENTSAWB",
    "Resident Saw II": "SIDEQUEST_RESIDENTSAW",
    "Sunset Flip Powerbomb": "SIDEQUEST_SUNSET_FLIP_POWERBOMB",
    "Balloon Mountain": "GRID_BALLOONLAIR",
    "Climbing Gym": "SIDEQUEST_BARREL_CLIMB",
    "Fisherman Suplex": "SIDEQUEST_FISHERMAN_SUPLEX",
    "STF": "SIDEQUEST_STF",
    "Arena": "SIDEQUEST_ARENASIXNINE",
    "Attitude Adjustment": "SIDEQUEST_ATTITUDE_ADJUSTMENT",
    "Rocket": "SIDEQUEST_ROCKETGODZ",
}

# fmt: on

def neon_white_get_locations() -> dict[str, int]:
    locations_dict: dict[str, int] = {}
    level_id = 500

    for normal_level in neon_white_levels_normal:
        for medal in neon_white_levels_medals:
            locations_dict[normal_level + " " + medal + " Completion"] = level_id
            level_id += 1
        locations_dict[normal_level + " Gift"] = level_id
        level_id += 1

    for giftless_level in neon_white_levels_giftless:
        for medal in neon_white_levels_medals:
            locations_dict[giftless_level + " " + medal + " Completion"] = level_id
            level_id += 1

    for sidequest_level in neon_white_levels_sidequests:
        locations_dict[sidequest_level + " Completion"] = level_id
        level_id += 1

    return locations_dict


checks_in_sets_lvl = {
                         lvl: {
                             lvl + " " + medal + " Completion" for medal in neon_white_levels_medals
                         } for lvl in neon_white_levels_normal
                     } | {
                         lvl: {
                             lvl + " Gift"
                         } for lvl in neon_white_levels_normal
                     } | {
                         lvl: {
                             lvl + " " + medal + " Completion" for medal in neon_white_levels_medals
                         } for lvl in neon_white_levels_giftless
                     } | {
                         lvl: {
                             lvl + " Completion"
                         } for lvl in neon_white_levels_sidequests
                     }
