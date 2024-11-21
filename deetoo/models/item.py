"""
Models covering itemization in Diablo 2.

https://diablo-archive.fandom.com/wiki/Items_(Diablo_II)
"""

from dataclasses import dataclass
from typing import Literal

from .base import (
    ItemBase,
    ItemType,
    WearableMixin,
    SocketableMixin,
    ClassSpecificMixin,
)


@dataclass
class Weapon(ItemBase, WearableMixin, SocketableMixin, ClassSpecificMixin):
    item_type: ItemType = "weapon"
    attack_speed: int = 0
    required_dexterity: int = 0
    one_hand_damage_min: int | None = 0
    one_hand_damage_max: int | None = 0
    weapon_class: Literal["axe", "mace", "bow", "dagger", "sword"] = "axe"


@dataclass
class ThrowWeapon(Weapon):
    item_type: ItemType = "throw_weapon"
    throw_damage_min: int = 0
    throw_damage_max: int = 0


@dataclass
class TwoHandWeapon(Weapon):
    item_type: ItemType = "two_handed_weapon"
    two_hand_damage_min: int = 0
    two_hand_damage_max: int = 0


@dataclass
class Armor(ItemBase, WearableMixin):
    defense_min: int = 0
    defense_max: int = 0


@dataclass
class Torso(Armor, SocketableMixin):
    item_type: ItemType = "torso"


@dataclass
class Helm(Armor, SocketableMixin, ClassSpecificMixin):
    item_type: ItemType = "torso"


@dataclass
class Belt(Armor):
    item_type: ItemType = "belt"
    potion_slots: int = 4


@dataclass
class Gloves(Armor):
    item_type: ItemType = "gloves"


@dataclass
class Shield(Armor, SocketableMixin, ClassSpecificMixin):
    item_type: ItemType = "shield"
    smite_damage_min: int = 0
    smite_damage_max: int = 0
    chance_to_block_pct: int = 0


@dataclass
class Boots(Armor):
    item_type: ItemType = "boots"
    kick_damage_min: int = 0
    kick_damage_max: int = 0


@dataclass
class Jewelry(ItemBase):
    item_type: str = "jewelry"


# Item is a broad type that supports the different shapes of data that are attributed
# to the items in Diablo 2.
Item = (
    Weapon | TwoHandWeapon | ThrowWeapon | Torso | Belt | Boots | Gloves | Helm | Shield
)

all = [
    Weapon,
    TwoHandWeapon,
    ThrowWeapon,
    Torso,
    Belt,
    Boots,
    Gloves,
    Helm,
    Shield,
]


# TODO: Gems, runes, jewels
#
# @dataclass
# class Charm(ItemBase): ...
#
# @dataclass
# class Insertable(ItemBase, InsertableMixin):
#     """
#     Gems and runes are insertable into socketed items.
#     """
#
# @dataclass
# class InsertableMixin:
#     """
#     Runes, gems, or jewels can be inserted into socketable items.
#     """

#     helm_affix: Affix
#     weapon_affix: Affix
#     shield_affix: Affix
#     armor_affix: Affix
#
# class Affix: ...
#
# @dataclass
# class Potion: ...
