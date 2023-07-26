from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from .base import metadata

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('name', String, nullable=False),
    Column('description', String, nullable=True, server_default=None),
    # Column('creation_time', DateTime, nullable=False),
    # Column('last_change', DateTime, nullable=True),
    # Column('active_until', DateTime, nullable=True),
    Column('is_active', Boolean, server_default=None),
    Column('is_admin', Boolean, server_default=None)
)
