import json
from argparse import ArgumentParser
from deetoo.models.v1.db import db_context
from thefuzz.fuzz import partial_ratio
from tinydb import Query


def fuzzy(val: str, search: str, threshold: int = 90) -> int:
    """
    Perform a fuzzy test
    """
    return partial_ratio(str(val), search) > threshold


if __name__ == "__main__":
    parser = ArgumentParser(usage='python search.py --query "sword"')
    parser.add_argument(
        "--query",
        "-q",
        default="sword",
        help="fuzzy search query term",
    )
    parser.add_argument("--fuzzy", "-f", action="store_true", default=False)
    parser.add_argument(
        "--key",
        "-k",
        default="name",
        help="the key to fuzzy search against",
    )
    args = parser.parse_args()

    with db_context("db.json") as db:
        base_items = db.table("base_items")
        unique_items = db.table("unique_items")

        if args.fuzzy:
            query = Query()[args.key].test(fuzzy, args.query)
        else:
            if args.query.isdigit():
                args.query = int(args.query)
            query = Query()[args.key] == args.query

        base_item_results = base_items.search(query)
        unique_item_results = unique_items.search(query)

        results = {
            "base_items": base_item_results,
            "unique_items": unique_item_results,
            "count": len(base_item_results) + len(unique_item_results),
        }
        print(json.dumps(results, indent=2, sort_keys=True))
