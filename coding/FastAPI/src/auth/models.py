from datetime import datetime
from sqlalchemy import (
    MetaData,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Table,
    Column,
    JSON,
    Boolean
)
from sqlalchemy.orm import mapped_column, Mapped
from fastapi_users.db import SQLAlchemyBaseUserTable 
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

metadata = MetaData()


# create tables
role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registed_at", TIMESTAMP, default=datetime.now()),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


Base: DeclarativeMeta = (declarative_base())  # stores metadata and used to created User Table Model
class User(SQLAlchemyBaseUserTable[int], Base):
    # our fields from DB
    id: Mapped[bool] = mapped_column(Integer, default=False, nullable=False, primary_key=True)
    name: Mapped[bool] = mapped_column(String, default=False, nullable=False)
    email: Mapped[bool] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    registed_at: Mapped[bool] = mapped_column(TIMESTAMP, default=datetime.now(), nullable=False)
    role_id: Mapped[bool] = mapped_column(Integer, ForeignKey(role.c.id))

    # these fields are required and cannot be deleted!
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)