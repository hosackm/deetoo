from enum import StrEnum
from pydantic import BaseModel
from typing import Literal


def item_type_to_class(item_type: str) -> type:
    map = {
        ItemType.BELT: BeltAttributes,
        ItemType.BOOTS: BootAttributes,
        ItemType.GLOVES: GlovesAttributes,
        ItemType.HELM: HelmAttributes,
        ItemType.JEWELRY: JewelryAttributes,
        ItemType.MISCELLANEOUS: MiscellaneousAttributes,
        ItemType.SHIELD: ShieldAttributes,
        ItemType.THROW_WEAPON: TwoHandedWeaponAttributes,
        ItemType.TORSO: TorsoAttributes,
        ItemType.TWO_HANDED_WEAPON: TwoHandedWeaponAttributes,
        ItemType.WEAPON: WeaponAttributes,
    }
    return map[item_type]


class ItemType(StrEnum):
    BELT = "belt"
    BOOTS = "boots"
    GLOVES = "gloves"
    HELM = "helm"
    JEWELRY = "jewelry"
    MISCELLANEOUS = "miscellaneous"
    SHIELD = "shield"
    THROW_WEAPON = "throw_weapon"
    TORSO = "torso"
    TWO_HANDED_WEAPON = "two_handed_weapon"
    WEAPON = "weapon"


CharClassType = Literal[
    "all",
    "amazon",
    "assassin",
    "barbarian",
    "druid",
    "necromancer",
    "paladin",
    "sorceress",
]

WeaponClassType = Literal[
    "amazonbow",
    "amazonjav",
    "amazonspear",
    "axe",
    "bow",
    "claw",
    "crossbow",
    "dagger",
    "javelin",
    "mace",
    "orb",
    "polearm",
    "scepter",
    "spear",
    "staff",
    "sword",
    "throw",
    "wand",
]

QualityType = Literal["normal", "exceptional", "elite"]


class BeltAttributes(BaseModel):
    required_level: int
    required_strength: int
    potion_slots: int
    quality: QualityType
    max_durability: int
    defense_min: int
    defense_max: int


class BootAttributes(BaseModel):
    required_level: int
    required_strength: int
    kick_damage_min: int
    kick_damage_max: int
    quality: QualityType
    max_durability: int
    defense_min: int
    defense_max: int


class GlovesAttributes(BaseModel):
    required_level: int
    required_strength: int
    max_durability: int
    defense_min: int
    defense_max: int
    quality: QualityType


class HelmAttributes(BaseModel):
    required_level: int
    required_strength: int
    max_durability: int
    defense_min: int
    defense_max: int
    max_sockets: int
    quality: QualityType
    char_class: CharClassType


class JewelryAttributes(BaseModel): ...


class MiscellaneousAttributes(BaseModel): ...


class ShieldAttributes(BaseModel):
    required_level: int
    required_strength: int
    max_sockets: int
    quality: QualityType
    max_durability: int
    defense_min: int
    defense_max: int
    smite_damage_min: int
    smite_damage_max: int
    chance_to_block_pct: int
    char_class: CharClassType


class ThrowWeaponAttributes(BaseModel):
    required_level: int
    required_strength: int
    required_dexterity: int
    attack_speed: int
    weapon_class: WeaponClassType
    one_hand_damage_min: int
    one_hand_damage_max: int
    throw_damage_min: int
    throw_damage_max: int
    quality: QualityType


class TorsoAttributes(BaseModel):
    required_level: int
    required_strength: int
    max_sockets: int
    quality: QualityType
    max_durability: int
    defense_min: int
    defense_max: int


class TwoHandedWeaponAttributes(BaseModel):
    required_level: int
    required_strength: int
    required_dexterity: int
    attack_speed: int
    weapon_class: WeaponClassType
    one_hand_damage_min: int
    one_hand_damage_max: int
    two_hand_damage_min: int
    two_hand_damage_max: int
    max_sockets: int
    quality: QualityType
    max_durability: int
    char_class: CharClassType


class WeaponAttributes(BaseModel):
    required_level: int
    required_strength: int
    required_dexterity: int
    attack_speed: int
    weapon_class: WeaponClassType
    one_hand_damage_min: int
    one_hand_damage_max: int
    max_sockets: int
    quality: QualityType
    max_durability: int
    char_class: CharClassType


item_type_to_cls = {
    ItemType.BELT: BeltAttributes,
    ItemType.BOOTS: BootAttributes,
    ItemType.GLOVES: GlovesAttributes,
    ItemType.HELM: HelmAttributes,
    ItemType.JEWELRY: JewelryAttributes,
    ItemType.MISCELLANEOUS: MiscellaneousAttributes,
    ItemType.SHIELD: ShieldAttributes,
    ItemType.THROW_WEAPON: TwoHandedWeaponAttributes,
    ItemType.TORSO: TorsoAttributes,
    ItemType.TWO_HANDED_WEAPON: TwoHandedWeaponAttributes,
    ItemType.WEAPON: WeaponAttributes,
}
