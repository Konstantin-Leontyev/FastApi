from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from endpoints.depends import get_users_repository
from repositories.users import UserRepository
from models.user import User, UserCreationResponse, UserUpdateResponse, UserDeletionResponse


router = APIRouter()


@router.get("/", response_model=List[User])
async def get_all_users(
        users: UserRepository = Depends(get_users_repository)):
    return await users.get_all_users()


@router.post("/", response_model=User)
async def get_user_by_id(
        user_id: int,
        users: UserRepository = Depends(get_users_repository)):
    return await users.get_user_by_id(user_id=user_id)


@router.put("/", response_model=UserCreationResponse)
async def create_user(
        user: User,
        users: UserRepository = Depends(get_users_repository)):
    return await users.create(user)


@router.patch("/", response_model=UserUpdateResponse)
async def update_user(
        user: User,
        users: UserRepository = Depends(get_users_repository)):
    response = await users.update(user)
    return response


@router.delete("/", response_model=UserDeletionResponse)
async def delete_user(
        user_id: int,
        users: UserRepository = Depends(get_users_repository)):
    return await users.delete_user_by_id(user_id=user_id)
