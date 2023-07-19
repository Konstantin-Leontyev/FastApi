from pydantic import BaseModel


class Pair(BaseModel):
    ticker: str
    pair_id: int
    price: float
