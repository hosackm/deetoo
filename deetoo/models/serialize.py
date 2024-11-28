from pydantic import BaseModel, Field, field_serializer
from deetoo.models.item import UniqueItem, Item


class ItemRead(BaseModel):
    id: int = Field(exclude=True)
    name: str
    attributes: dict

    class Config:
        from_attributes = True


class UniqueItemRead(BaseModel):
    id: int = Field(exclude=True)
    name: str
    base_item_id: int = Field(exclude=True)
    base_item: ItemRead | None

    class Config:
        from_attributes = True


class SetRead(BaseModel):
    id: int = Field(exclude=True)
    name: str


class SetItemRead(BaseModel):
    id: int = Field(exclude=True)
    name: str
    base_item_id: int = Field(exclude=True)
    base_item: ItemRead | None
    set_id: int = Field(exclude=True)
    set: SetRead | None  # converted to str during serialization

    class Config:
        from_attributes = True

    @field_serializer("set")
    def serialize_set(self, set: SetRead, _info):
        return set.name


if __name__ == "__main__":
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.orm import joinedload
    from sqlmodel.ext.asyncio.session import AsyncSession
    from deetoo.models import sqlite_url
    from sqlmodel import select
    import asyncio

    async def main():
        engine = create_async_engine(sqlite_url)
        session = AsyncSession(engine)
        result = await session.exec(
            select(UniqueItem).options(joinedload(UniqueItem.base_item))
        )
        print([UniqueItemRead.model_validate(r) for r in result.all()])
        await session.close()

    asyncio.run(main())
