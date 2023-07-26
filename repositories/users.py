from datetime import datetime

from fastapi import HTTPException
from starlette import status
from db.users import users
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_all_users(self):
        """ Returns users list """
        query = users.select().limit(100)
        return await self.database.fetch_all(query)

    async def get_user_by_id(self, user_id: int):
        """ Returns user by id """
        query = users.select().where(users.c.id == user_id)
        user = await self.database.fetch_one(query=query)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No user with this id")

        return user

    async def create(self, user: User) -> dict:
        """ Create user """
        query = users.select().where(users.c.id == user.id)
        existing_user = await self.database.fetch_one(query)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")

        new_user = User(
            id=user.id,
            name=user.name,
            description=user.description if user.description else None,
            # creation_time=datetime.now(),
            # last_change=user.last_change,
            # active_until=user.active_until,
            is_active=user.is_active,
            is_admin=user.is_admin,
        )

        values = {**new_user.model_dump()}
        query = users.insert().values(**values)
        try:
            await self.database.execute(query=query)
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User creation request error")
        else:
            return {"status": 'OK',
                    "message": "New user was successfully created",
                    "new_user": user}

    async def update(self, user: User) -> dict:
        """ Update user """
        user_id = user.id

        updated_user = User(
            id=user.id,
            name=user.name,
            description=user.description,
            # creation_time=datetime.now(),
            # last_change=user.last_change,
            # active_until=user.active_until,
            is_active=user.is_active,
            is_admin=user.is_admin,
        )

        values = {**updated_user.model_dump()}
        query = users.update().where(users.c.id == user_id).values(**values)
        try:
            await self.database.execute(query=query)
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                                detail="User update request error")
        else:
            return {"status": 'OK',
                    "message": "User was successfully updated",
                    "updated_user": updated_user}

    async def delete_user_by_id(self, user_id: int):
        """ Delete user by id"""
        query = users.select().where(users.c.id == user_id)
        deleted_user = await self.database.fetch_one(query=query)
        if deleted_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No user with this id")

        query = users.delete().where(users.c.id == user_id)
        try:
            await self.database.execute(query=query)
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User deletion request error")
        else:
            return {"status": 'OK',
                    "message": "User was successfully deleted",
                    "deleted_user": deleted_user}
