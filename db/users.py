import sqlalchemy
from .base import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("telegram_id", sqlalchemy.BIGINT, primary_key=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False, server_default="Alex"),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("active_until", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("is_active", sqlalchemy.BOOLEAN, server_default='false'),
    sqlalchemy.Column("is_admin", sqlalchemy.BOOLEAN, server_default='false')
)
