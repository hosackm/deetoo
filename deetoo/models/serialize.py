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
    def serialize_dt(self, set: SetRead, _info):
        return set.name


if __name__ == "__main__":
    from sqlmodel import Session, select
    from sqlalchemy.orm import joinedload
    from deetoo.models import get_engine

    with Session(get_engine()) as session:
        result = session.exec(
            select(UniqueItem).options(joinedload(UniqueItem.base_item))
        ).first()
        print(UniqueItemRead.serialize(result))
        result = session.exec(select(Item)).first()
        print(ItemRead.serialize(result))
