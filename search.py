import json
from argparse import ArgumentParser
from deetoo.models.db import db_context
from thefuzz.fuzz import partial_ratio
from tinydb import Query


def fuzzy(val: str, search: str, threshold: int = 90) -> int:
    """
    Perform a fuzzy test
    """
    return partial_ratio(val, search) > threshold


if __name__ == "__main__":
    parser = ArgumentParser(usage='python search.py --query "sword"')
    parser.add_argument(
        "--query",
        "-q",
        default="sword",
        help="fuzzy search query term",
    )
    args = parser.parse_args()

    with db_context("db.json") as db:
        base_items = db.table("base_items")
        swords = base_items.search(Query().name.test(fuzzy, args.query))
        print(json.dumps(swords, indent=2, sort_keys=True))
