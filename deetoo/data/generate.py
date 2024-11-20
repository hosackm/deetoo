"""
Build the TinyDB database from the provided csv files.
"""

from argparse import ArgumentParser
from csv import reader
from pathlib import Path
from tinydb import TinyDB
from deetoo.models.item import (
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


DATA_FOLDER = Path(__file__).parent.resolve()
CSV_FOLDER = DATA_FOLDER / "csv"


def parse_csv_to_class(filename, cls):
    objects = []
    with open(filename) as f:
        rdr = reader(f)
        headers = next(rdr)
        for row in rdr:
            row = [None if col == "null" else col for col in row]
            objects.append(cls(**dict(zip(headers, row))))
    return objects


def read_data():
    """
    Reads all item csv files and returns a dictionary containing their
    contents as deetoo.models.item dataclass dictionaries that
    can be serialized as json.
    """
    mappers = [
        (Path("weapon.csv"), Weapon),
        (Path("two_handed_weapon.csv"), TwoHandWeapon),
        (Path("throw_weapon.csv"), ThrowWeapon),
        (Path("torso.csv"), Torso),
        (Path("belt.csv"), Belt),
        (Path("boots.csv"), Boots),
        (Path("gloves.csv"), Gloves),
        (Path("helm.csv"), Helm),
        (Path("shield.csv"), Shield),
    ]
    items = []
    for path, cls in mappers:
        items.extend(el.json for el in parse_csv_to_class(CSV_FOLDER / path, cls))
    return items


def write_database(filepath):
    if filepath.exists():
        filepath.unlink()

    db = TinyDB(filepath)
    base_items = db.table("base_items")
    base_items.insert_multiple(read_data())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--filename", "-f", default="db.json")
    args = parser.parse_args()
    write_database(Path(args.filename))
