from contextlib import asynccontextmanager
from deetoo.models import sqlite_url
from deetoo.models.item import Item, UniqueItem, SetItem, Set
from deetoo.models.serialize import ItemRead, UniqueItemRead, SetItemRead, SetRead
from fastapi import FastAPI, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import create_async_engine

import logging

logger = logging.getLogger("uvicorn")


def cache_lookup(request: Request):
    if request.url.path in request.app.cache:
        logger.info(f"Cache hit: {request.url.path}")
        return request.app.cache[request.url.path]

    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Pre-loading cache with values from: {sqlite_url}")
    app.cache = Cache()
    await app.cache.load_cache()
    yield


class Cache:
    def __init__(self):
        self.store = {}

    def __getitem__(self, key, default=None):
        return self.store.get(key, default)

    def __contains__(self, key):
        return key in self.store

    async def load_cache(self):
        self.engine = create_async_engine(sqlite_url)
        self.session = AsyncSession(self.engine)
        await self.load()
        await self.session.close()

    async def load(self):
        queries = [
            ("/base_items", select(Item), ItemRead),
            (
                "/unique_items",
                select(UniqueItem).options(joinedload(UniqueItem.base_item)),
                UniqueItemRead,
            ),
            (
                "/set_items",
                select(SetItem).options(
                    joinedload(SetItem.base_item), joinedload(SetItem.set)
                ),
                SetItemRead,
            ),
            ("/sets", select(Set), SetRead),
        ]

        for key, query, model in queries:
            rows = await self.session.exec(query)
            models = [model.model_validate(r, from_attributes=True) for r in rows]
            for m in models:
                self.store[f"{key}/{m.id}"] = m
            self.store[key] = models
