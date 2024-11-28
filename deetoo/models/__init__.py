from pathlib import Path
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

dbpath = Path(__file__).resolve().parents[2] / "sqlmodel.db"
sqlite_url = f"sqlite+aiosqlite:///{dbpath}"


def init_db(url=sqlite_url):
    SQLModel.metadata.create_all(get_engine(url, echo=True))


def get_engine(url=sqlite_url, echo=False):
    return create_engine(url, echo=echo)


async def get_session() -> AsyncGenerator[AsyncSession]:
    engine = create_async_engine(sqlite_url)
    async with AsyncSession(engine) as session:
        yield session
