from pathlib import Path
from csv import reader


from deetoo.models import get_engine
from deetoo.models.item import Item, UniqueItem, Set, SetItem
from sqlmodel import Session
from sqlalchemy import text


DATA_DIR = Path(__file__).resolve().parent / "csv"


def read_base_items():
    """
    Read base items from .csv and return as list of dicts.
    """
    filenames = (
        "weapon.csv",
        "two_handed_weapon.csv",
        "belt.csv",
        "boots.csv",
        "gloves.csv",
        "helm.csv",
        "jewelry.csv",
        "shield.csv",
        "throw_weapon.csv",
        "torso.csv",
    )

    items = {}
    for filename in filenames:
        with open(DATA_DIR / filename) as f:
            rdr = reader(f)
            headers = next(rdr)
            for row in rdr:
                name = row[0]
                blob = dict(zip(headers[1:], row[1:]))
                items[name] = Item(name=name, blob=blob)

    return items


def read_unique_items(name_to_base_item):
    """
    Read uniques from .csv and return as list of dicts. Lookup
    the base item's id in the name_to_base_item dict.
    """
    uniques = []
    with open(DATA_DIR / "uniques.csv") as f:
        rdr = reader(f)
        next(rdr)
        for row in rdr:
            u = UniqueItem(name=row[0], base_item=name_to_base_item[row[1]])
            uniques.append(u)
    return uniques


def read_set_items(name_to_base_item):
    """
    Read set items from .csv and return as list of dicts. Lookup
    the base item's id in the name_to_base_item dict. Return a list of
    set names as well.
    """
    set_items = []
    sets = {}
    with open(DATA_DIR / "set_items.csv") as f:
        rdr = reader(f)
        next(rdr)
        for row in rdr:
            name, set_name, base_name = row
            if set_name not in sets:
                sets[set_name] = Set(name=set_name)

            set_items.append(
                SetItem(
                    name=name,
                    base_item=name_to_base_item[base_name],
                    set=sets[set_name],
                )
            )
    return set_items, sets


def main():
    base_item_map = read_base_items()
    uniques = read_unique_items(base_item_map)
    set_items, set_map = read_set_items(base_item_map)
    engine = get_engine()

    with Session(engine) as session:
        session.exec(text("DELETE FROM items"))
        session.exec(text("DELETE FROM unique_items"))
        session.exec(text("DELETE FROM set_items"))
        session.exec(text("DELETE FROM sets"))

    all_adds = list(base_item_map.values())
    all_adds += uniques
    all_adds += list(set_map.values())
    all_adds += set_items
    with Session(engine) as session:
        for a in all_adds:
            session.add(a)
        session.commit()


if __name__ == "__main__":
    main()