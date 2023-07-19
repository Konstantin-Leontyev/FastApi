from fastapi import HTTPException
from starlette import status
from db.users import users
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_all(self):
        query = users.select().limit(100)
        return await self.database.fetch_all(query)

    async def get_user_by_telegram_id(self, telegram_id: int):
        query = users.select().where(users.c.telegram_id == telegram_id)

        user = await self.database.fetch_one(query)

        if user is None:
            raise HTTPException(status_code=404,
                                detail="No user with this id")

        return User.model_validate(user)

    async def create(self, u: User):
        # -
        query = users.select().where(users.c.telegram_id == u.telegram_id)
        existing_user = await self.database.fetch_one(query)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")
        # -
        user = User(
            telegram_id=u.telegram_id,
            name=u.name,
            description=u.description,
            active_until=u.active_until,
            is_active=u.is_active,
            is_admin=u.is_admin,
            # last_action=datetime.datetime.utcnow()
        )

        values = {**user.model_dump()}
        query = users.insert().values(**values)
        try:
            await self.database.execute(query)
        except User.CreationError:
            raise HTTPException(status_code=404,
                                detail="User creation error")
        else:
            return user

    async def update(self, u: User) -> User:
        telegram_id = u.telegram_id

        user = User(
            telegram_id=u.telegram_id,
            name=u.name,
            description=u.description,
            active_until=u.active_until,
            is_active=u.is_active,
            is_admin=u.is_admin,
            # last_action=datetime.datetime.utcnow()
        )

        values = {**user.model_dump()}

        query = users.update().where(users.c.telegram_id == telegram_id).values(**values)
        await self.database.execute(query)
        return user

    async def delete(self, telegram_id: int):
        query = users.delete().where(users.c.telegram_id == telegram_id)
        await self.database.execute(query=query)
        return {"status": True}
