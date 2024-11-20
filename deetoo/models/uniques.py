from dataclasses import dataclass


@dataclass
class UniqueItem:
    """
    A unique version of a base item.

    TODO:
        * affixes for each unique item
    """

    name: str = ""
    base_item_ref: int = 0
    # ... affixes
