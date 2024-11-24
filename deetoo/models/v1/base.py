from typing import Literal
from dataclasses import dataclass, asdict

CharClass = Literal[
    "all",
    "amazon",
    "assassin",
    "barbarian",
    "druid",
    "paladin",
    "necromancer",
    "sorceress",
]

ItemType = Literal[
    "belt",
    "boots",
    "gloves",
    "helm",
    "jewelry",
    "shield",
    "throw_weapon",
    "torso",
    "two_handed_weapon",
    "weapon",
]


class JSONEncodeMixin:
    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return self.__dict__


@dataclass
class ItemBase(JSONEncodeMixin):
    name: str = ""
    required_level: int = 0
    item_type: ItemType = ""


@dataclass
class WearableMixin:
    """
    Characters can wear weapons, armor, shields, etc.
    """

    required_strength: int = 0
    max_durability: int = 0
    quality: Literal["normal", "exceptional", "elite"] = "normal"


@dataclass
class SocketableMixin:
    """
    Weapons, shield, helms, and armor can have items inserted into sockets.
    """

    max_sockets: int = 0


@dataclass
class ClassSpecificMixin:
    """
    Weapons, shield, and helms can be specific to a certain character class.
    """

    char_class: CharClass = "all"
