from dataclasses import dataclass


from .base import ItemBase


@dataclass
class UniqueItem(ItemBase):
    """
    A unique version of a base item.

    TODO:
        * affixes for each unique item

        See: https://diablo-archive.fandom.com/wiki/Affixes_(Diablo_II)
    """

    name: str = ""
    required_level: int = 0
    base_item_ref: int = 0
