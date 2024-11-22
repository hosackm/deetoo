"""
Build the TinyDB database from the provided csv files.
"""

from argparse import ArgumentParser
from csv import reader
from pathlib import Path
from tinydb import TinyDB, Query
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


def process_str(val):
    if val.isdigit():
        return int(val)
    elif val == "null":
        return None
    return val


def parse_csv_to_class(filename, cls, post_process_func=None, db=None):
    objects = []
    with open(filename) as f:
        rdr = reader(f)
        headers = next(rdr)
        for row in rdr:
            data = {key: process_str(val) for key, val in zip(headers, row)}
            if post_process_func:
                data = post_process_func(db, data)
            objects.append(cls(**data))
    return objects


def read_base_items_data(db=None, post_process_func=None):
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
    return [
        el.json
        for el in parse_csv_to_class(
            CSV_FOLDER / "uniques.csv", UniqueItem, resolve_base_reference, db
        )
    ]


def resolve_base_reference(db, data):
    """
    Lookup the referred base item by name and copy out its values into
    data. Delete base_item_name key before returning.
    """
    base_item = db.table("base_items").get(Query().name == data["base_item_name"])
    data["base_item_ref"] = base_item.doc_id
    data["item_type"] = base_item["item_type"]
    del data["base_item_name"]
    return data


def write_database(filepath):
    filepath.unlink(missing_ok=True)

    db = TinyDB(filepath)

    # base items
    base_items = db.table("base_items")
    base_items.insert_multiple(read_base_items_data())

    # unique items
    unique_table = db.table("unique_items")
    unique_items = read_unique_items_data(db)
    unique_table.insert_multiple(unique_items)

    # TODO: sets


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--filename", "-f", default="db.json")
    args = parser.parse_args()
    write_database(Path(args.filename))
