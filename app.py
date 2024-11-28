from fastapi import FastAPI, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from deetoo.models import get_session
from deetoo.models.item import Item, UniqueItem, Set, SetItem
from deetoo.models.serialize import UniqueItemRead, ItemRead, SetItemRead, SetRead

app = FastAPI()


@app.get("/base_items/{item_id}")
async def get_item(
    item_id: int,
    session: AsyncSession = Depends(get_session),
) -> ItemRead:
    result = await session.exec(select(Item).where(Item.id == item_id))
    return result.first()


@app.get("/base_items")
async def get_items(
    q: str = None,
    session: AsyncSession = Depends(get_session),
) -> list[ItemRead]:
    query = select(Item)
    if q:
        query = query.where(Item.name.ilike(f"%{q}%"))
    return (await session.exec(query)).all()


@app.get("/unique_items/{item_id}")
async def get_unique_item(
    item_id: int,
    session: AsyncSession = Depends(get_session),
) -> UniqueItemRead:
    query = (
        select(UniqueItem)
        .where(UniqueItem.id == item_id)
        .options(joinedload(UniqueItem.base_item))
    )
    result = await session.exec(query)
    return result.first()


@app.get("/unique_items")
async def get_unique_items(
    q: str = None,
    session: AsyncSession = Depends(get_session),
) -> list[UniqueItemRead]:
    query = select(UniqueItem).options(joinedload(UniqueItem.base_item))
    if q:
        query = query.where(UniqueItem.name.ilike(f"%{q}%"))
    return (await session.exec(query)).all()


@app.get("/set_items/{item}")
async def get_set_item(
    item: int,
    session: AsyncSession = Depends(get_session),
) -> SetItemRead:
    query = (
        select(SetItem)
        .where(SetItem.id == item)
        .options(
            joinedload(SetItem.base_item),
            joinedload(SetItem.set),
        )
    )
    return (await session.exec(query)).first()


@app.get("/set_items")
async def get_set_items(
    q: str = None,
    session: AsyncSession = Depends(get_session),
) -> list[SetItemRead]:
    query = select(SetItem).options(
        joinedload(SetItem.base_item),
        joinedload(SetItem.set),
    )
    if q:
        query = query.where(SetItem.name.ilike(f"%{q}%"))
    return (await session.exec(query)).all()


@app.get("/sets/{set_id}")
async def get_set(
    set_id: int,
    session: AsyncSession = Depends(get_session),
) -> SetRead:
    return (await session.exec(select(Set).where(Set.id == set_id))).first()


@app.get("/sets")
async def get_sets(
    q: str = None, session: AsyncSession = Depends(get_session)
) -> list[SetRead]:
    query = select(Set)
    if q:
        query = query.where(Set.name.ilike(f"%{q}%"))
    return (await session.exec(query)).all()
