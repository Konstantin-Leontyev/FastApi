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

    async def get_user_by_telegram_id(self, telegram_id: int):
        """ Returns user by id """
        query = users.select().where(users.c.telegram_id == telegram_id)
        user = await self.database.fetch_one(query=query)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No user with this id")

        return user

    async def create(self, user: User):
        """ Create user """
        query = users.select().where(users.c.telegram_id == user.telegram_id)
        existing_user = await self.database.fetch_one(query)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")

        new_user = User(
            telegram_id=user.telegram_id,
            name=user.name,
            description=user.description,
            active_until=user.active_until,
            is_active=user.is_active,
            is_admin=user.is_admin,
            # last_action=datetime.datetime.utcnow()
        )

        values = {**new_user.model_dump()}
        query = users.insert().values(**values)
        try:
            await self.database.execute(query=query)
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User creation request error")
        else:
            return new_user

    async def update(self, user: User) -> User:
        """ Update user """
        telegram_id = user.telegram_id

        updated_user = User(
            telegram_id=user.telegram_id,
            name=user.name,
            description=user.description,
            active_until=user.active_until,
            is_active=user.is_active,
            is_admin=user.is_admin,
            # last_action=datetime.datetime.utcnow()
        )

        values = {**updated_user.model_dump()}
        query = users.update().where(users.c.telegram_id == telegram_id).values(**values)
        try:
            await self.database.execute(query=query)
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                                detail="User update request error")
        else:
            return updated_user

    async def delete_user_by_id(self, telegram_id: int):
        """ Delete user by id"""
        query = users.delete().where(users.c.telegram_id == telegram_id)
        user = await users.get_user_by_telegram_id(telegram_id=telegram_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        try:
            await self.database.execute(query=query)
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User deletion request error")
        else:
            return {"status": True}
