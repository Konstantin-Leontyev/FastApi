from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from endpoints.depends import get_pairs_repository
from repositories.pairs import PairRepository
from models.pair import Pair


router = APIRouter()


@router.get("/", response_model=List[Pair])
async def get_all_pairs(
        pairs: PairRepository = Depends(get_pairs_repository)):
    return await pairs.get_all()


@router.post("/", response_model=Pair)
async def get_pair_by_id(
        pair_id: int,
        pairs: PairRepository = Depends(get_pairs_repository)):
    return await pairs.get_pair_by_id(pair_id=pair_id)


@router.post("/", response_model=Pair)
async def get_pair_by_ticker(
        ticker: str,
        pairs: PairRepository = Depends(get_pairs_repository)):
    return await pairs.get_pair_by_ticker(ticker=ticker)


@router.put("/", response_model=Pair)
async def create_pair(
        pair: Pair,
        pairs: PairRepository = Depends(get_pairs_repository)):
    return await pairs.create(pair)


@router.patch("/", response_model=Pair)
async def update_pair(
        pair: Pair,
        pairs: PairRepository = Depends(get_pairs_repository)):
    return await pairs.update(pair)


@router.delete("/")
async def delete_pair_by_id(
        pair_id: int,
        pairs: PairRepository = Depends(get_pairs_repository)):
    pair = await pairs.get_pair_by_id(pair_id=pair_id)
    if pair is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pair not found")

    return await pairs.delete_pair_by_id(pair_id=pair_id)


@router.delete("/")
async def delete_pair_by_ticker(
        ticker: str,
        pairs: PairRepository = Depends(get_pairs_repository)):
    pair = await pairs.get_pair_by_ticker(ticker=ticker)
    if pair is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pair not found")

    return await pairs.delete_pair_by_ticker(ticker=ticker)
