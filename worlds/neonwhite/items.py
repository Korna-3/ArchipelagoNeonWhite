from collections.abc import Iterable
from typing import NamedTuple

from BaseClasses import Item, ItemClassification


class NWItem(Item):
    game: str = "Neon White"

class NWItemData(NamedTuple):
    category: str
    id: int
    classification: ItemClassification

def get_items_from_category(category: str) -> Iterable[str]:
    for name, item in nw_items.items():
        if item.category == category:
            yield name

nw_items: dict[str, NWItemData] = {

    "Katana":               NWItemData("Card", 501, ItemClassification.progression | ItemClassification.useful),
    "Book of Life":         NWItemData("Card", 502, ItemClassification.progression | ItemClassification.useful),
    "Purify - Fire":        NWItemData("Card", 503, ItemClassification.progression | ItemClassification.useful),
    "Purify - Discard":     NWItemData("Card", 504, ItemClassification.progression | ItemClassification.useful),
    "Elevate - Fire":       NWItemData("Card", 505, ItemClassification.progression | ItemClassification.useful),
    "Elevate - Discard":    NWItemData("Card", 506, ItemClassification.progression | ItemClassification.useful),
    "Godspeed - Fire":      NWItemData("Card", 507, ItemClassification.progression | ItemClassification.useful),
    "Godspeed - Discard":   NWItemData("Card", 508, ItemClassification.progression | ItemClassification.useful),
    "Stomp - Fire":         NWItemData("Card", 509, ItemClassification.progression | ItemClassification.useful),
    "Stomp - Discard":      NWItemData("Card", 510, ItemClassification.progression | ItemClassification.useful),
    "Fireball - Fire":      NWItemData("Card", 511, ItemClassification.progression | ItemClassification.useful),
    "Fireball - Discard":   NWItemData("Card", 512, ItemClassification.progression | ItemClassification.useful),
    "Dominion - Fire":      NWItemData("Card", 513, ItemClassification.progression | ItemClassification.useful),
    "Dominion - Discard":   NWItemData("Card", 514, ItemClassification.progression | ItemClassification.useful),

    "Neon Rank":            NWItemData("Progression", 515, ItemClassification.progression_skip_balancing),
    "Mission Unlock":       NWItemData("Progression", 516, ItemClassification.progression),

    "Heavenly Delight Ticket": NWItemData("Filler", 517, ItemClassification.filler | ItemClassification.useful)
}

item_categories = [
    "Progression",
    "Card",
    "Filler"
]

nw_item_groups = { cat: set(get_items_from_category(cat)) for cat in item_categories }
