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
    Jewelry,
)
from deetoo.models.unique import UniqueItem


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


def read_base_items_data():
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
        (Path("jewelry.csv"), Jewelry),
    ]
    items = []
    for path, cls in mappers:
        items.extend(el.json for el in parse_csv_to_class(CSV_FOLDER / path, cls))
    return items


def read_unique_items_data(db):
    """
    Read unique data has to do a lookup on the existing base items and get
    their doc_id as a reference.
    """
    uniques = []
    base_item_name_to_id = {
        doc["name"]: (doc_id, doc["item_type"])
        for doc_id, doc in enumerate(db.table("base_items").all(), 1)
    }
    with open(CSV_FOLDER / "uniques.csv") as f:
        rdr = reader(f)
        headers = next(rdr)
        for row in rdr:
            kwargs = extract_base_information(
                dict(zip(headers, row)),
                base_item_name_to_id,
            )
            uniques.append(UniqueItem(**kwargs).json)
    return uniques


def extract_base_information(data, mapping):
    """
    Replace lookup the base item's `doc_id` and `item_type` in the
    mapping and replace them in the provided data dictionary.
    """
    base_item_name = data.get("base_item_name")
    doc_id, doc_item_type = mapping.get(base_item_name)
    data["base_item_ref"] = doc_id
    data["item_type"] = doc_item_type
    del data["base_item_name"]
    return data


def write_database(filepath):
    filepath.unlink(missing_ok=True)

    db = TinyDB(filepath)

    # base items
    base_items = db.table("base_items")
    base_items.insert_multiple(read_base_items_data())

    # unique items
    unique_items = db.table("unique_items")
    unique_items.insert_multiple(read_unique_items_data(db))

    # TODO: sets


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--filename", "-f", default="db.json")
    args = parser.parse_args()
    write_database(Path(args.filename))
