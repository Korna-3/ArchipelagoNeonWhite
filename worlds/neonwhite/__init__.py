import base64
import io
import json
import zlib
from typing import Any

from BaseClasses import Tutorial
from rule_builder.rules import CanReachLocation
from worlds.AutoWorld import WebWorld, World

from .items import NWItem, get_items_from_category, nw_item_groups, nw_items
from .locations import checks_in_sets_lvl, neon_white_get_locations, neon_white_level_name_internal

#from .Locations import PTLocation, pt_locations, pt_location_groups
from .options import NeonWhiteOptions
from .regions import create_regions
from .rules import LevelRequirements, LevelRequirementSet, Medal, get_mission_rank_required, set_rules


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

    item_name_to_id = {name: data.id for name, data in nw_items.items()}  # noqa: RUF012

    location_name_to_id = neon_white_get_locations()

    item_name_groups = nw_item_groups
    location_name_groups = checks_in_sets_lvl

    ordered_levels: list[str]   # Post-rando level list, to be split into missions every 11 levels
    ranks_required: int

    requirements: LevelRequirementSet

    origin_region_name = "Central Heaven"

    web = NeonWhiteWeb()

    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise Exception("Neon White yaml's slot name has invalid character(s).")

        ut_regen = getattr(self.multiworld, "re_gen_passthrough", {})
        if (self.game in ut_regen):
            ut_regen = ut_regen[self.game]
            self.ordered_levels = ut_regen["levels"]
            self.options.rank_requirement.value = ut_regen["rank_requirement"]
            self.options.mission_count.value = ut_regen["mission_count"]
            self.options.medal_cap.value = ut_regen["medal_cap"]
            self.options.difficulty.value = ut_regen["difficulty"]

        self.ordered_levels = []

    def create_item(self, name: str) -> NWItem:
        return NWItem(name, nw_items[name].classification, nw_items[name].id, self.player)

    def create_regions(self):
        create_regions(self.player, self.multiworld, self.options)

    def create_items(self):
        itempool = []

        loc_count = len(self.get_locations())  # pyright: ignore[reportArgumentType]

        # Add soul cards
        itempool += [self.create_item(card) for card in get_items_from_category("Card")]

        # Make sure we add the neon ranks that we need
        self.ranks_required = ((loc_count - len(itempool)) * (self.options.rank_requirement / 100))
        itempool += [self.create_item("Neon Rank")] * get_mission_rank_required(self, self.options.mission_count.value)

        # Fill the rest with filler
        itempool += [self.create_filler() for _ in range(loc_count - len(itempool))]

        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        # 1/100 items added for filler will be a miracle katana, the rest will be neon rank increments
        if self.multiworld.random.randint(1, 100) == 100:
            return "Miracle Katana"
        return "Neon Rank"

    def set_rules(self):
        set_rules(self.multiworld, self, self.options)
        self.set_completion_rule(CanReachLocation("Absolution Ace Completion"))

    def fill_slot_data(self):
        logic = io.BytesIO()
        for level in self.ordered_levels:
            for medal in reversed(range(self.options.medal_cap)): # reversed to compress better
                reqs = self.requirements.get_necessary_items(level, Medal(medal))
                logic.write(len(reqs).to_bytes(byteorder="little"))
                if LevelRequirements.FistOnly in reqs:
                    reqs = set(LevelRequirements.FistOnly)

                for req in reqs:
                    logic.write(req.value.to_bytes(2, "little"))

            reqs = self.requirements.get_necessary_items(level, Medal.Gift)
            logic.write(len(reqs).to_bytes())

            for req in reqs:
                logic.write(req.to_bytes(2, "little"))

        cpobj = zlib.compressobj(level=9, wbits=-15, memLevel=9)
        encoded_logic = base64.a85encode(cpobj.compress(logic.getvalue()) + cpobj.flush()).decode()
        # print(encoded_logic)
        # print(len(encoded_logic))
        # print(len(logic.getvalue()))

        dumps = json.dumps([neon_white_level_name_internal[x] for x in self.ordered_levels], separators=(",", ":"))

        cpobj = zlib.compressobj(level=9, wbits=-15, memLevel=9)
        encoded_levels = base64.a85encode(cpobj.compress(dumps.encode()) + cpobj.flush()).decode()
        # print(len(encoded_levels))
        # print(len(dumps))

        return {
            "level_order": encoded_levels,
            "level_logic": encoded_logic,
            "mission_costs": [
                get_mission_rank_required(self, i + 1)
                    for i in range(self.options.mission_count)
            ],
            "options": self.options.as_dict("difficulty", "medal_cap", "death_link")
        }

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any]:
        reverse = {v: k for k, v in neon_white_level_name_internal.items()}

        dcobj = zlib.decompressobj(-15)
        decoded = json.loads(dcobj.decompress(base64.a85decode(slot_data["level_order"])) + dcobj.flush())

        return {
            "levels": [reverse[x] for x in decoded],
            "rank_requirement": slot_data["mission_costs"][-1],
            "mission_count": len(slot_data["mission_costs"]),
            "medal_cap": slot_data["options"]["medal_cap"],
            "difficulty": slot_data["options"]["difficulty"]
        }
