from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from deetoo.models import get_session
from deetoo.models.item import Item, UniqueItem, Set, SetItem
from deetoo.models.serialize import UniqueItemRead, ItemRead, SetItemRead, SetRead
from deetoo.cache import lifespan, cache_lookup


app = FastAPI(lifespan=lifespan)


@app.get("/base_items/{item_id}")
async def get_item(
    item_id: int,
    cache_lookup: ItemRead | None = Depends(cache_lookup),
) -> ItemRead:
    if not cache_lookup:
        raise HTTPException(status_code=404, detail=f"item {item_id} not found")
    return cache_lookup


@app.get("/base_items")
async def get_items(
    q: str = None,
    cache_lookup: list[ItemRead] | None = Depends(cache_lookup),
    session: AsyncSession = Depends(get_session),
) -> list[ItemRead]:
    if cache_lookup:
        return cache_lookup

    query = select(Item)
    if q:
        query = query.where(Item.name.ilike(f"%{q}%"))
    return (await session.exec(query)).all()


@app.get("/unique_items/{item_id}")
async def get_unique_item(
    item_id: int,
    cache_lookup: UniqueItemRead | None = Depends(cache_lookup),
    session: AsyncSession = Depends(get_session),
) -> UniqueItemRead:
    if cache_lookup:
        return cache_lookup

    query = (
        select(UniqueItem)
        .where(UniqueItem.id == item_id)
        .options(joinedload(UniqueItem.base_item))
    )
    result = await session.exec(query)
    item = result.one_or_none()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"unique item with id {item_id} not found."
        )
    return item


@app.get("/unique_items")
async def get_unique_items(
    q: str = None,
    cache_lookup: list[UniqueItemRead] | None = Depends(cache_lookup),
    session: AsyncSession = Depends(get_session),
) -> list[UniqueItemRead]:
    if cache_lookup:
        return cache_lookup

    query = select(UniqueItem).options(joinedload(UniqueItem.base_item))
    if q:
        query = query.where(UniqueItem.name.ilike(f"%{q}%"))
    return (await session.exec(query)).all()


@app.get("/set_items/{item_id}")
async def get_set_item(
    item_id: int,
    cache_lookup: SetItemRead | None = Depends(cache_lookup),
    session: AsyncSession = Depends(get_session),
) -> SetItemRead:
    if cache_lookup:
        return cache_lookup

    query = (
        select(SetItem)
        .where(SetItem.id == item_id)
        .options(
            joinedload(SetItem.base_item),
            joinedload(SetItem.set),
        )
    )
    item = (await session.exec(query)).one_or_none()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"set item item with id {item_id} not found."
        )


@app.get("/set_items")
async def get_set_items(
    q: str = None,
    cache_lookup: list[SetItemRead] | None = Depends(cache_lookup),
    session: AsyncSession = Depends(get_session),
) -> list[SetItemRead]:
    if cache_lookup:
        return cache_lookup

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
    cache_lookup: SetRead | None = Depends(cache_lookup),
    session: AsyncSession = Depends(get_session),
) -> SetRead:
    if cache_lookup:
        return cache_lookup

    item = (await session.exec(select(Set).where(Set.id == set_id))).one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail=f"set with id {set_id} not found.")

    return (await session.exec(select(Set).where(Set.id == set_id))).first()


@app.get("/sets")
async def get_sets(
    q: str = None,
    cache_lookup: list[SetRead] | None = Depends(cache_lookup),
    session: AsyncSession = Depends(get_session),
) -> list[SetRead]:
    if cache_lookup:
        return cache_lookup

    query = select(Set)
    if q:
        query = query.where(Set.name.ilike(f"%{q}%"))
    return (await session.exec(query)).all()
