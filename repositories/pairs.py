from fastapi import HTTPException

from db.pairs import pairs
from models.pair import Pair
from repositories.base import BaseRepository


class PairRepository(BaseRepository):
    async def get_all(self):
        query = pairs.select()
        return await self.database.fetch_all(query)

    async def get_pair_by_id(self, pair_id: int):
        query = pairs.select().where(pairs.c.pair_id == pair_id)
        pair = await self.database.fetch_one(query)

        if pair is None:
            raise HTTPException(status_code=404,
                                detail="No pair with this id")

        return Pair.model_validate(pair)

    async def get_pair_by_ticker(self, ticker: str):
        query = pairs.select().where(pairs.c.ticker == ticker)
        pair = await self.database.fetch_one(query)

        if pair is None:
            raise HTTPException(status_code=404,
                                detail="No pair with this ticker")

        return Pair.model_validate(pair)

    async def create(self, s: Pair):
        pair = Pair(
            ticker=s.ticker,
            price=s.price
        )

        values = {**pair.model_dump()}
        query = pairs.insert().values(**values)

        try:
            await self.database.execute(query)
        except Pair.CreationError:
            raise HTTPException(status_code=404,
                                detail="Pair creation error")
        else:
            return pair

    async def update(self, s: Pair):
        pair = s.ticker

        symbol = Pair(
            pair=s.ticker,
            price=s.price
        )

        values = {**symbol.model_dump()}

        query = pairs.update().where(pairs.c.ticker == pair).values(**values)
        try:
            await self.database.execute(query)
        except Pair.UpdateError:
            raise HTTPException(status_code=404,
                                detail="Pair update error")
        else:
            return pair

    async def delete_pair_by_id(self, pair_id: int):
        query = pairs.delete().where(pairs.c.pair_id == pair_id)
        try:
            await self.database.execute(query)
        except Pair.DeletionError:
            raise HTTPException(status_code=404,
                                detail="Pair deletion error")
        else:
            return {"status": True}

    async def delete_pair_by_ticker(self, ticker: str):
        query = pairs.delete().where(pairs.c.ticker == ticker)
        try:
            await self.database.execute(query)
        except Pair.DeletioneError:
            raise HTTPException(status_code=404,
                                detail="Pair deletion error")
        else:
            return {"status": True}
