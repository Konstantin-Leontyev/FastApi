from .users import users
from .pairs import pairs
from .base import metadata, engine

metadata.create_all(bind=engine)
