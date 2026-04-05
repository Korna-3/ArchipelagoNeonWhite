import csv
import itertools
from enum import IntEnum, IntFlag, auto
from math import floor
from typing import TYPE_CHECKING

from BaseClasses import MultiWorld
from rule_builder.rules import False_, Has, HasAll, True_
from worlds.neonwhite import NeonWhiteOptions
from worlds.neonwhite.locations import (
    neon_white_levels_giftless,
    neon_white_levels_medals,
    neon_white_levels_normal,
    neon_white_levels_sidequests,
)
from worlds.neonwhite.options import Difficulty, MedalCap

from . import data

if TYPE_CHECKING:
    from rule_builder.rules import Rule

    from . import NeonWhiteWorld

class Medal(IntEnum):
    Bronze = 0
    Silver = 1
    Gold = 2
    Ace = 3
    Dev = 4
    Gift = 5

# ruff: disable[E701]
# fmt: off
def medal_from_medal_cap(medal_cap: MedalCap) -> Medal:
    match int(medal_cap):
        case 1: return Medal.Bronze
        case 2: return Medal.Silver
        case 3: return Medal.Gold
        case 4: return Medal.Ace
        case 5: return Medal.Dev
        case _: return Medal.Bronze
# ruff: enable[E701]
# fmt: on

class LevelRequirements(IntFlag):
    FistOnly = 0
    Katana = auto()
    PurifyFire = auto()
    PurifyDiscard = auto()
    ElevateFire = auto()
    ElevateDiscard = auto()
    GodspeedFire = auto()
    GodspeedDiscard = auto()
    StompFire = auto()
    StompDiscard = auto()
    FireballFire = auto()
    FireballDiscard = auto()
    DominionFire = auto()
    DominionDiscard = auto()
    BookOfLife = auto()

    @staticmethod
    def solo_to_string(solo: "LevelRequirements") -> str | None:
        if not solo.name:
            return None
        if (solo.name.endswith("Fire")):
            return solo.name.removesuffix("Fire") + " - Fire"
        if (solo.name.endswith("Discard")):
            return solo.name.removesuffix("Discard") + " - Discard"
        if solo == LevelRequirements.Katana:
            return "Katana"
        if solo == LevelRequirements.BookOfLife:
            return "Book of Life"
        return None # fists?

    @staticmethod
    def string_to_solo(string: str) -> "LevelRequirements":
        if (string.endswith("- Fire")):
            return LevelRequirements[string.split(maxsplit=1)[0] + "Fire"]
        if (string.endswith("- Discard")):
            return LevelRequirements[string.split(maxsplit=1)[0] + "Discard"]
        if string == "Katana":
            return LevelRequirements.Katana
        if string == "Book of Life":
            return LevelRequirements.BookOfLife
        return LevelRequirements.FistOnly

    def to_list(self) -> list[str]:
        if self == LevelRequirements.FistOnly:
            return []
        return [LevelRequirements.solo_to_string(x) for x in LevelRequirements if x in self]  # pyright: ignore[reportReturnType]

    @staticmethod
    def from_list(lst: list[str]) -> "LevelRequirements":
        ret = LevelRequirements.FistOnly
        for x in lst:
            ret |= LevelRequirements.string_to_solo(x)
        return ret


# This only represents a single difficulty
class LevelRequirementSet:
    def __init__(self, levels: list[str]):
        # String is the level name, list is 0..5, in order: dev,ace,gold,bronze,silver,gift
        self.requirements = dict[str, list[set[LevelRequirements]]]()
        for level in levels:
            self.requirements[level] = [
                set[LevelRequirements](),
                set[LevelRequirements](),
                set[LevelRequirements](),
                set[LevelRequirements](),
                set[LevelRequirements](),
                set[LevelRequirements]()]

    # Note - Medal 0-4 is dev-bronze, 5 is gift
    # Cards are what is available at that point
    def can_complete_level(self, level: str, medal: Medal, cards: LevelRequirements) -> bool:
        medal_idx = int(medal) if medal == Medal.Gift else 4 - int(medal)

        for solution in self.requirements[level][medal_idx]:
            # Bitwise check, e.g. 0001 & 1111 == 0001, success; 1001 & 0101 == 0001, failure
            # If Fist-Only is a solution, & will return 0 (because it's all zeroes) and thus will == 0, always success
            if solution & cards == solution:
                return True
        return False

    def make_rule(self, level: str, medal: Medal) -> "Rule":
        medal_idx = int(medal) if medal == Medal.Gift else 4 - int(medal)
        rule = False_()

        for solution in self.requirements[level][medal_idx]:
            if (solution == LevelRequirements.FistOnly):
                return True_()

            rule |= HasAll(*solution.to_list())
        return rule


    def get_necessary_items(self, level:str, medal:Medal) -> list[LevelRequirements]:
        medal_idx = int(medal) if medal == Medal.Gift else 4 - int(medal)
        return list(self.requirements[level][medal_idx])



def string_to_level_req_flag(level: str) -> LevelRequirements:
    match level:
        case "Kf":
            return LevelRequirements.Katana
        case "Pf":
            return LevelRequirements.PurifyFire
        case "Pd":
            return LevelRequirements.PurifyDiscard
        case "Ef":
            return LevelRequirements.ElevateFire
        case "Ed":
            return LevelRequirements.ElevateDiscard
        case "Gf":
            return LevelRequirements.GodspeedFire
        case "Gd":
            return LevelRequirements.GodspeedDiscard
        case "Sf":
            return LevelRequirements.StompFire
        case "Sd":
            return LevelRequirements.StompDiscard
        case "Ff":
            return LevelRequirements.FireballFire
        case "Fd":
            return LevelRequirements.FireballDiscard
        case "Df":
            return LevelRequirements.DominionFire
        case "Dd":
            return LevelRequirements.DominionDiscard
        case "Bd":
            return LevelRequirements.BookOfLife
        case _:
            # Unexpected symbol/fist only
            return LevelRequirements.FistOnly

def import_csv_to_data(diff: Difficulty) -> LevelRequirementSet:
    # See archipelago requirements sheet for formatting
    from importlib.resources import files
    file = files(data).joinpath("nw_cr.csv").open()
    csv_reader = csv.reader(file)
    csv_iter = iter(csv_reader)
    # Grab names, cells are merged and encompass the 4 difficulties so only take every multiple of 4
    level_names: list[str] = next(csv_iter)[0::4]
    new_requirements = LevelRequirementSet(level_names)  # Return value that will be filled
    medal_idx = 0  # 0 == Dev, 1 == Ace, ... 5 == Gift
    for row in csv_iter:
        for i in range(0, len(level_names)):
            level_name = level_names[i]
            # First copy any requirements from the medal above (unless it's the gift row)
            # Doesn't matter if there's mixed combos, that's dealt with (e.g. Ef and Ef+Ed can exist together)
            if medal_idx != 5:
                for j in range(0, medal_idx):
                    new_requirements.requirements[level_name][medal_idx] |= new_requirements.requirements[level_name][j]
            # Copy requirements from all easier difficulties
            # Requirements are checked as a "can beat x with these weapons?" so this works
            for j in range(0, diff):
                # The csv can be cut off prematurely as export to csv wraps when reaching final cell of a row
                # Causes OOB error for any non-easy difficulty if final entry has empty cols, so clamp index for same result
                cell_idx = min((i * 4) + j, len(row) - 1)
                cell = row[cell_idx]
                # F means fist completable, no requirements
                if cell == "F":
                    new_requirements.requirements[level_name][medal_idx].add(LevelRequirements.FistOnly)
                else:
                    for solution in cell.split('|'):
                        requirements_aggregate = LevelRequirements(LevelRequirements.FistOnly)
                        for requirement in solution.split(","):
                            requirements_aggregate |= string_to_level_req_flag(requirement)
                        if requirements_aggregate != LevelRequirements.FistOnly:
                            new_requirements.requirements[level_name][medal_idx].add(requirements_aggregate)
        medal_idx = medal_idx + 1
    return new_requirements

# Actual functions related to rules start here
def level_rando(world: "NeonWhiteWorld", requirements: LevelRequirementSet) -> list[str]:
    # TODO: Make this smarter, e.g. fill levels on a gradient from smallest minimum requirement to most

    level_queue = neon_white_levels_normal + neon_white_levels_giftless + neon_white_levels_sidequests
    level_queue.remove("Absolution") # This will always be placed at the end

    # Place 2 levels where the gift and gold medal can be obtained Fist-Only at the very start
    fist_only_levels = []
    for level in level_queue:
        if level not in neon_white_levels_normal:
            continue
        if requirements.can_complete_level(level, Medal.Gold, LevelRequirements.FistOnly) and requirements.can_complete_level(level, Medal.Gift, LevelRequirements.FistOnly):
            fist_only_levels.append(level)
    world.random.shuffle(fist_only_levels)
    for i in range(2):
        level_queue.remove(fist_only_levels[i])
    fist_only_levels = fist_only_levels[:2]

    # Shuffle the rest, append, then put Absolution at the end
    world.random.shuffle(level_queue)
    return fist_only_levels + level_queue + ["Absolution"]

# Mission is 1-indexed
def get_required_rank_for_mission(total_rank_count: int, mission: int, mission_count: int) -> int:
    # Neon rank requirement is exponential, requiring a tiny number of neon ranks for the first missions but quickly increasing
    # total_rank_count /= 10
    mission_fraction = mission / mission_count
    lenience_value = 10
    normal_value = (pow(lenience_value, mission_fraction) - 1) / (lenience_value - 1)
    return floor(total_rank_count * normal_value)

def set_rules(multiworld: MultiWorld, world: "NeonWhiteWorld", options: NeonWhiteOptions):
    requirements = import_csv_to_data(options.difficulty)

    medal_cap_typed = medal_from_medal_cap(options.medal_cap)

    if not world.ordered_levels:
        world.ordered_levels = level_rando(world, requirements)

    levels_norm = len(world.ordered_levels) // world.mission_count
    offset = world.mission_count - (len(world.ordered_levels) % world.mission_count)

    # Place one relevant discard ability into the early items pool to give the player something to work with
    relevant_discards: set[str] = set()
    for i in range(levels_norm):
        for solution in itertools.chain(requirements.get_necessary_items(world.ordered_levels[i], medal_cap_typed), requirements.get_necessary_items(world.ordered_levels[i], Medal.Gift)):
            for card in solution:
                cardstr = LevelRequirements.solo_to_string(card)
                if cardstr and ("Discard" in cardstr or "Book of Life" in cardstr):
                    relevant_discards.add(cardstr)
    relevant_discards_list = list(relevant_discards)
    multiworld.local_early_items[world.player][relevant_discards_list[world.random.randint(0, len(relevant_discards_list) - 1)]] = 1

    central_heaven = world.get_region("Central Heaven")
    # Connect central heaven to every mission
    level_total = 0
    for i in range(world.mission_count):
        mission_region = world.get_region(f"Mission {i + 1}")
        entrance_name = f"Central Heaven to Mission {i + 1}"
        central_heaven.connect(mission_region, entrance_name)
        if i != 0:
            neonrank_count = get_required_rank_for_mission(world.rank_requirement, i + 1, world.mission_count)
            world.set_rule(world.get_entrance(entrance_name), Has("Neon Rank", neonrank_count))

        # Connect each mission to the levels they contain
        level_count = levels_norm
        if (i >= offset):
            level_count += 1

        for _ in range(level_count):
            level_name = world.ordered_levels[level_total]
            level_total += 1
            mission_region.connect(multiworld.get_region(level_name, world.player),
                f"{mission_region.name} to {level_name}")
            if level_name in neon_white_levels_normal or level_name in neon_white_levels_giftless:
                for medal in range(options.medal_cap):
                    world.set_rule(world.get_location(f"{level_name} {neon_white_levels_medals[medal]} Completion"),
                        requirements.make_rule(level_name, Medal(medal)))

                if level_name not in neon_white_levels_giftless:
                    world.set_rule(world.get_location(level_name + " Gift"),
                        requirements.make_rule(level_name, Medal.Gift))

            else:
                world.set_rule(world.get_location(level_name + " Completion"),
                    requirements.make_rule(level_name, Medal.Dev))

    from Utils import visualize_regions
    visualize_regions(central_heaven, "neon_white_regions.puml")
