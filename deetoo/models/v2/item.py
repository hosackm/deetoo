from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.sqlite import JSON

from .base import Base


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    blob: Mapped[dict] = mapped_column(JSON, default={})
    uniques: Mapped[list["UniqueItem"]] = relationship(
        "UniqueItem",
        back_populates="base_item",
    )
    set_items: Mapped[list["SetItem"]] = relationship(
        "SetItem",
        back_populates="base_item",
    )


class SetItem(Base):
    __tablename__ = "set_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    base_item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    base_item: Mapped[Item] = relationship("Item", back_populates="set_items")
    set_id: Mapped[int] = mapped_column(ForeignKey("sets.id"))
    set: Mapped["Set"] = relationship("Set", back_populates="items")


class Set(Base):
    __tablename__ = "sets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    items: Mapped[list[SetItem]] = relationship("SetItem", back_populates="set")


class UniqueItem(Base):
    __tablename__ = "unique_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    base_item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    base_item: Mapped[Item] = relationship("Item", back_populates="uniques")
