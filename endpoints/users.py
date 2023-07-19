from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from endpoints.depends import get_users_repository
from repositories.users import UserRepository
from models.user import User


router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(
        users: UserRepository = Depends(get_users_repository),
):
    return await users.get_all()


@router.post("/", response_model=User)
async def get_user_by_telegram_id(
        telegram_id: int,
        users: UserRepository = Depends(get_users_repository)):
    return await users.get_user_by_telegram_id(telegram_id=telegram_id)


@router.put("/", response_model=User)
async def create_user(
        user: User,
        users: UserRepository = Depends(get_users_repository)):
    return await users.create(user)


@router.patch("/", response_model=User)
async def update_user(
        user: User,
        users: UserRepository = Depends(get_users_repository)):
    return await users.update(user)


@router.delete("/")
async def delete_user(
        telegram_id: int,
        users: UserRepository = Depends(get_users_repository)):
    user = await users.get_user_by_telegram_id(telegram_id=telegram_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await users.delete(telegram_id=telegram_id)
