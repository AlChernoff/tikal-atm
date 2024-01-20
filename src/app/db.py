import os

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    Float,
    create_engine
)
from databases import Database
from sqlalchemy.engine import base

DATABASE_URL: str = os.getenv("DATABASE_URL")

# SQLAlchemy
engine: base.Engine = create_engine(DATABASE_URL)
metadata: MetaData = MetaData()
inventory: Table = Table(
    "inventory",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String(50)),
    Column("value", Float, nullable=False),
    Column("amount", Integer, nullable=False),
)

# databases query builder
database: Database = Database(DATABASE_URL)
