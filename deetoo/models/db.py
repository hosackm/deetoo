from pathlib import Path
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from contextlib import contextmanager


def get_database(filepath=Path("items.json")):
    return TinyDB(filepath, storage=CachingMiddleware(JSONStorage))


@contextmanager
def db_context(filepath=Path("items.json")):
    """
    Return the database wrapped in a context manager for safe closing behavior.
    """
    with TinyDB(filepath, storage=CachingMiddleware(JSONStorage)) as db:
        yield db
