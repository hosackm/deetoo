from dataclasses import dataclass


@dataclass
class SetItem:
    """
    A single item within a set.

    TODO:
        * affixes for each item
    """

    name: str = ""
    base_item_ref: int = 0
    # ... affixes


@dataclass
class Set:
    """
    A collection of set items that form a complete set.

    TODO:
        * set bonuses - 2 pieces, 3, 4, etc.
    """

    name: str = ""
    items: list[SetItem]
