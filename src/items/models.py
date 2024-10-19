from sqlalchemy import Table, Column, Integer, String

from src.database import metadata

item = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String),
    Column("image", String),
    Column("description", String),
    Column("price", Integer),
    Column("size", String),
)
