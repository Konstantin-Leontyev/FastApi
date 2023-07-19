import sqlalchemy
from .base import metadata

pairs = sqlalchemy.Table(
    "pairs",
    metadata,
    sqlalchemy.Column("ticker", sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column("pair_id", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("price", sqlalchemy.REAL, nullable=False, server_default="0")
)