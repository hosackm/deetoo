from pathlib import Path
from sqlmodel import create_engine, SQLModel

dbpath = Path(__file__).resolve().parents[2] / "sqlmodel.db"
sqlite_url = f"sqlite:///{dbpath}"
engine = create_engine(sqlite_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
