import datetime
from pydantic import BaseModel


class User(BaseModel):
    telegram_id: int
    name: str = 'Alex'
    description: str = None
    active_until: datetime.datetime = datetime.datetime.utcnow()
    is_active: bool = False
    is_admin: bool = False
