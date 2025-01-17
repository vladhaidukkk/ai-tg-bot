from decimal import Decimal

from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ModelBase(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(table_name)s_%(column_0_N_name)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class User(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    balance: Mapped[Decimal] = mapped_column(server_default="0")


class AIType(ModelBase):
    __tablename__ = "ai_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class AIModel(ModelBase):
    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("ai_types.id"))
    price: Mapped[Decimal]
