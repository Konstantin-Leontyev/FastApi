from repositories.users import UserRepository
from repositories.pairs import PairRepository
from db.base import database


def get_users_repository() -> UserRepository:
    return UserRepository(database)


def get_pairs_repository() -> PairRepository:
    return PairRepository(database)
