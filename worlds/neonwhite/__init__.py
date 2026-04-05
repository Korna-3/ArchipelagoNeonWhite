from typing import Any

from BaseClasses import Tutorial
from rule_builder.rules import CanReachLocation
from worlds.AutoWorld import WebWorld, World

from .items import NWItem, get_items_from_category, nw_item_groups, nw_items
from .locations import checks_in_sets_lvl, neon_white_get_locations, neon_white_level_name_internal

#from .Locations import PTLocation, pt_locations, pt_location_groups
from .options import NeonWhiteOptions
from .regions import create_regions
from .rules import get_required_rank_for_mission, set_rules


class NeonWhiteWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Neon White integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Badhamknibbs"]
    )]
    #theme = "partyTime"
    bug_report_page = "https://github.com/Badhamknibbs/ArchipelagoNeonWhite/issues"


# Keeping World slim so that it's easier to comprehend
class NeonWhiteWorld(World):
    """
    Neon White is a speedrunning FPS puzzle platformer made by freaks for freaks.
    Rush through a series of levels making smart use of your restricted cards to clear heaven of demons.
    """

    game = "Neon White"
    options: NeonWhiteOptions  # pyright: ignore[reportIncompatibleVariableOverride]
    options_dataclass = NeonWhiteOptions

    item_name_to_id = {name: data.id for name, data in nw_items.items()}

    location_name_to_id = neon_white_get_locations()

    item_name_groups = nw_item_groups
    location_name_groups = checks_in_sets_lvl

    ordered_levels: list[str]   # Post-rando level list, to be split into missions every 11 levels
    rank_requirement: int
    mission_count: int

    origin_region_name = "Central Heaven"

    web = NeonWhiteWeb()

    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise Exception("Neon White yaml's slot name has invalid character(s).")

        self.rank_requirement = self.options.rank_requirement.value
        self.mission_count = self.options.mission_count.value

        self.ordered_levels = []

    def create_item(self, name: str) -> NWItem:
        return NWItem(name, nw_items[name].classification, nw_items[name].id, self.player)

    def create_regions(self):
        create_regions(self.player, self.multiworld, self.options)

    def create_items(self):
        itempool = []

        loc_count = len(self.get_locations())

        # Add soul cards
        for card in get_items_from_category("Card"):
            itempool.append(self.create_item(card))

        # Make sure we add the neon ranks that we need
        itempool.extend([self.create_item("Neon Rank")] * self.rank_requirement)

        # Fill the rest with filler
        for _ in range(loc_count - len(itempool)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        # 1/100 items added for filler will be a miracle katana, the rest will be neon rank increments
        if self.multiworld.random.randint(1, 100) == 100:
            return "Miracle Katana"
        return "Neon Rank"

    def set_rules(self):
        ut_regen = getattr(self.multiworld, "re_gen_passthrough", {})
        if (self.game in ut_regen):
            ut_regen = ut_regen[self.game]
            self.ordered_levels = ut_regen["levels"]
            self.rank_requirement = ut_regen["options"]["rank_requirement"]
            self.mission_count = ut_regen["options"]["mission_count"]


        set_rules(self.multiworld, self, self.options)
        self.set_completion_rule(CanReachLocation("Absolution Ace Completion"))

    def fill_slot_data(self):
        return {
            "level_order": [neon_white_level_name_internal[level] for level in self.ordered_levels],
            "rank_increments": int(self.rank_requirement),
            "mission_costs": [
                get_required_rank_for_mission(self.rank_requirement, i + 1, self.mission_count)
                    for i in range(self.mission_count)
            ]
        }

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any]:
        reverse = {v: k for k, v in neon_white_level_name_internal.items()}
        return {
            "levels": [reverse[x] for x in slot_data["level_order"]],
            "options": self.options.as_dict("rank_requirement", "mission_count")
        }
