from sqlmodel import SQLModel, Field, Relationship, CheckConstraint
from typing import Optional
from sqlalchemy import Column, JSON
from .schema import ItemType


ItemTypeConstraint = CheckConstraint(
    name="item_type_constraint",
    sqltext=f"item_type IN ({','.join(f"'{i}'" for i in ItemType)})",
)


class Item(SQLModel, table=True):
    __tablename__ = "items"
    __table_args__ = (ItemTypeConstraint,)

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    item_type: str
    blob: dict = Field(sa_column=Column(JSON))

    set_items: list["SetItem"] = Relationship(back_populates="base_item")
    unique_items: list["UniqueItem"] = Relationship(back_populates="base_item")


class SetItem(SQLModel, table=True):
    __tablename__ = "set_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    base_item_id: int | None = Field(default=None, foreign_key="items.id")
    base_item: Item | None = Relationship(back_populates="set_items")

    set_id: int | None = Field(default=None, foreign_key="sets.id")
    set: Optional["Set"] | None = Relationship(back_populates="items")


class Set(SQLModel, table=True):
    __tablename__ = "sets"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    items: list[SetItem] = Relationship(back_populates="set")


class UniqueItem(SQLModel, table=True):
    __tablename__ = "unique_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    base_item_id: int | None = Field(default=None, foreign_key="items.id")
    base_item: Item | None = Relationship(back_populates="unique_items")
