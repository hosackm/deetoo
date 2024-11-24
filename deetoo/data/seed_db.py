import json
from csv import reader
from pathlib import Path

from deetoo.models.v2.db import engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker


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

    items = []
    for filename in filenames:
        with open(DATA_DIR / filename) as f:
            rdr = reader(f)
            headers = next(rdr)
            for row in rdr:
                items.append(
                    dict(
                        name=row[0],
                        blob=json.dumps(dict(zip(headers[1:], row[1:]))),
                    )
                )

    return items


def read_uniques(name_to_id):
    """
    Read uniques from .csv and return as list of dicts. Lookup
    the base item's id in the name_to_id dict.
    """
    uniques = []
    with open(DATA_DIR / "uniques.csv") as f:
        rdr = reader(f)
        next(rdr)  # headers
        for row in rdr:
            uniques.append(
                {
                    "name": row[0],
                    "base_item_id": name_to_id[row[1]],
                }
            )
    return uniques


def read_set_items(name_to_id):
    """
    Read set items from .csv and return as list of dicts. Lookup
    the base item's id in the name_to_id dict. Return a list of
    set names as well.
    """
    set_items = []
    sets = set()
    with open(DATA_DIR / "set_items.csv") as f:
        rdr = reader(f)
        next(rdr)  # headers
        for row in rdr:
            set_items.append(
                {
                    "name": row[0],
                    "set_name": row[1],
                    "base_item_id": name_to_id[row[2]],
                }
            )
            sets.add(row[1])
    return set_items, list(sets)


def drop_items(session):
    with session.begin():
        session.execute(sa.text("DELETE FROM items"))
        session.execute(sa.text("DELETE FROM unique_items"))
        session.execute(sa.text("DELETE FROM set_items"))
        session.execute(sa.text("DELETE FROM sets"))


def insert_base_items(session):
    base_items = read_base_items()
    ids = []

    with session.begin():
        sql_text = sa.text("INSERT INTO items(name, blob) VALUES(:name, :blob)")
        for item in base_items:
            session.execute(sql_text, item)
            result = session.execute(sa.text("SELECT last_insert_rowid()")).scalar()
            ids.append(result)

    return {d["name"]: id for id, d in zip(ids, base_items)}


def insert_unique_items(session, name_to_id):
    uniques = read_uniques(name_to_id)

    with session.begin():
        sql_text = sa.text("""
            INSERT INTO unique_items(name, base_item_id)
            VALUES(:name, :base_item_id)
        """)
        session.execute(sql_text, uniques)


def insert_set_items(session, name_to_id):
    set_items, sets = read_set_items(name_to_id)
    set_name_to_id = {}

    # insert sets and get set ids after each insertion
    with session.begin():
        sql_text = sa.text("INSERT INTO sets(name) VALUES(:name)")
        for s in sets:
            session.execute(sql_text, [{"name": s}])
            result = session.execute(sa.text("SELECT last_insert_rowid()")).scalar()
            set_name_to_id[s] = result

    # insert set items referencing the newly inserted set ids
    values = [
        {
            "name": item["name"],
            "base_item_id": item["base_item_id"],
            "set_id": set_name_to_id[item["set_name"]],
        }
        for item in set_items
    ]
    with session.begin():
        sql_text = sa.text("""
            INSERT INTO set_items(name, base_item_id, set_id)
            VALUES(:name, :base_item_id, :set_id)
        """)
        session.execute(sql_text, values)

    return set_name_to_id


def main():
    session = sessionmaker(engine)()
    drop_items(session)
    name_to_id = insert_base_items(session)
    insert_unique_items(session, name_to_id)
    insert_set_items(session, name_to_id)


if __name__ == "__main__":
    main()
