from argparse import ArgumentParser
import json
from sqlmodel import Session, select

from deetoo.models import get_engine
from deetoo.models.item import Item, SetItem, UniqueItem


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

    with Session(get_engine()) as session:
        like = f"%{args.query}%"
        results = session.exec(select(Item).where(Item.name.ilike(like))).all()
        base_results = [b.model_dump() for b in results]

        results = session.exec(
            select(SetItem, Item)
            .join(Item)
            .where(
                Item.name.ilike(like),
            )
        ).all()
        s_results: list[SetItem] = [s.model_dump() for s, _ in results]

        results = session.exec(
            select(UniqueItem, Item)
            .join(Item)
            .where(
                Item.name.ilike(like),
            )
        ).all()
        u_results: list[UniqueItem] = [u.model_dump() for u, _ in results]

        print(
            json.dumps(
                {
                    "base_items": {
                        "count": len(base_results),
                        "results": base_results,
                    },
                    "unique_items": {
                        "count": len(u_results),
                        "results": u_results,
                    },
                    "set_items": {
                        "count": len(s_results),
                        "results": s_results,
                    },
                }
            )
        )
