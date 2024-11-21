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
        unique_items = db.table("unique_items")

        results = {
            "base_items": base_items.search(Query().name.test(fuzzy, args.query)),
            "unique_items": unique_items.search(Query().name.test(fuzzy, args.query)),
        }
        results["count"] = len(results["base_items"]) + len(results["unique_items"])
        print(json.dumps(results, indent=2, sort_keys=True))
