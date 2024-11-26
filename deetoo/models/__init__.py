from pathlib import Path
from sqlmodel import create_engine, SQLModel

dbpath = Path(__file__).resolve().parents[2] / "sqlmodel.db"
sqlite_url = f"sqlite:///{dbpath}"


def init_db():
    SQLModel.metadata.create_all(get_engine(echo=True))


def get_engine(echo=False):
    return create_engine(sqlite_url, echo=echo)
