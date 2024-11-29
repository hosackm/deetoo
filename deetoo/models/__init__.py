from pathlib import Path
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

dbpath = Path(__file__).resolve().parents[2] / "deetoo.db"
sqlite_url = f"sqlite+aiosqlite:///{dbpath}"


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_engine(url=sqlite_url, echo=False):
    return create_engine(url, echo=echo)


async def get_session() -> AsyncGenerator[AsyncSession]:
    engine = create_async_engine(sqlite_url)
    async with AsyncSession(engine) as session:
        yield session
