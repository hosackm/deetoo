import json
import pytest

from deetoo.models.v1.item import (
    Weapon,
    TwoHandWeapon,
    ThrowWeapon,
    Torso,
    Belt,
    Boots,
    Gloves,
    Helm,
    Shield,
)

c = [Weapon, TwoHandWeapon, ThrowWeapon, Torso, Belt, Boots, Gloves, Helm, Shield]


@pytest.mark.parametrize("cls", c)
def test_can_json_serialize(cls):
    obj = cls()
    data = obj.__dict__
    assert json.loads(json.dumps(data)) == data
