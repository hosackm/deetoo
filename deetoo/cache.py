from fastapi import FastAPI, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager

from deetoo.models import sqlite_url
from deetoo.models.item import Item, UniqueItem, SetItem, Set
from deetoo.models.serialize import ItemRead, UniqueItemRead, SetItemRead, SetRead
from sqlmodel import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import create_async_engine

import logging

logger = logging.getLogger("uvicorn")

cache = {}


def cache_lookup(request: Request):
    key = request.url.path
    if key in cache:
        logger.info(f"Cache hit: {key}")
        return cache[key]
    return None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info(f"Pre-loading cache with values from: {sqlite_url}")
    await load_cache()
    yield


async def load_cache():
    engine = create_async_engine(sqlite_url)
    session = AsyncSession(engine)

    global cache
    await load_base_items(session, cache)
    await load_unique_items(session, cache)
    await load_set_items(session, cache)
    await load_sets(session, cache)

    await session.close()


async def load_base_items(session, cache):
    results = (await session.exec(select(Item))).all()
    base_results = [ItemRead.model_validate(r) for r in results]
    for r in base_results:
        cache[f"/base_items/{r.id}"] = r
    cache["/base_items"] = base_results


async def load_unique_items(session, cache):
    results = (
        await session.exec(select(UniqueItem).options(joinedload(UniqueItem.base_item)))
    ).all()
    unique_results = [UniqueItemRead.model_validate(r) for r in results]
    for r in unique_results:
        cache[f"/unique_items/{r.id}"] = r
    cache["/unique_items"] = unique_results


async def load_set_items(session, cache):
    results = (
        await session.exec(
            select(SetItem).options(
                joinedload(SetItem.base_item),
                joinedload(SetItem.set),
            )
        )
    ).all()

    set_results = [SetItemRead.model_validate(r, from_attributes=True) for r in results]
    for r in set_results:
        cache[f"/set_items/{r.id}"] = r
    cache["/set_items"] = set_results


async def load_sets(session, cache):
    results = (await session.exec(select(Set))).all()
    set_results = [SetRead.model_validate(r, from_attributes=True) for r in results]

    for r in set_results:
        cache[f"/sets/{r.id}"] = r
    cache["/sets"] = set_results
