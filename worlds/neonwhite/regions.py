from BaseClasses import MultiWorld, Region

from .locations import (
    NWLocation,
    neon_white_get_locations,
    neon_white_levels_giftless,
    neon_white_levels_medals,
    neon_white_levels_normal,
    neon_white_levels_sidequests,
)
from .options import NeonWhiteOptions


def create_regions(player: int, multiworld: MultiWorld, options: NeonWhiteOptions):
    # 121 levels split into 11 missions of 11 levels, differing from the base game
    mission_list = [f"Mission {x + 1}" for x in range(options.mission_count)]
    heaven_regions: list[Region] = [Region("Central Heaven", player, multiworld, None)]

    neon_white_locations = neon_white_get_locations()

    # Create regions and add locations
    heaven_regions.extend([Region(mission, player, multiworld) for mission in mission_list])

    for level in neon_white_levels_normal:
        check_region = Region(level, player, multiworld)
        for medal in range(options.medal_cap):
            check_name = level + " " + neon_white_levels_medals[medal] + " Completion"
            new_location = NWLocation(player, check_name, neon_white_locations[check_name], check_region)
            check_region.locations.append(new_location)
        check_name = level + " Gift"
        new_location = NWLocation(player, check_name, neon_white_locations[check_name], check_region)
        check_region.locations.append(new_location)
        heaven_regions.append(check_region)

    for level in neon_white_levels_giftless:
        check_region = Region(level, player, multiworld)
        for medal in range(options.medal_cap):
            check_name = level + " " + neon_white_levels_medals[medal] + " Completion"
            new_location = NWLocation(player, check_name, neon_white_locations[check_name], check_region)
            check_region.locations.append(new_location)
        heaven_regions.append(check_region)

    for level in neon_white_levels_sidequests:
        check_region = Region(level, player, multiworld)
        check_name = level + " Completion"
        new_location = NWLocation(player, check_name, neon_white_locations[check_name], check_region)
        check_region.locations.append(new_location)
        heaven_regions.append(check_region)

    multiworld.regions += heaven_regions
