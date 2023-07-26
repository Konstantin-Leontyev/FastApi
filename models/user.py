from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    description: Optional[str]
    # creation_time: datetime
    # last_change: Optional[datetime]
    # active_until: Optional[datetime]
    is_active: bool = Optional[bool]
    is_admin: bool = Optional[bool]


class UserCreationResponse(BaseModel):
    status: str = 'OK'
    message: str = 'New user was successfully created'
    new_user: User


class UserUpdateResponse(BaseModel):
    status: str = 'OK'
    message: str = 'User was successfully updated'
    updated_user: User


class UserDeletionResponse(BaseModel):
    status: str = 'OK'
    message: str = 'User was successfully deleted'
    deleted_user: User
