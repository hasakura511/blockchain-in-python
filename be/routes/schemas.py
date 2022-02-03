from typing import List, Dict
from pydantic import BaseModel


class Block(BaseModel):
    timestamp: int
    difficulty: int
    nonce: int
    data: List[dict] = []
    hash: str
    last_hash: str

    # class Config:
    #     orm_mode = True


class Wallet(BaseModel):
    address: str
    balance: float


class Blockchain(BaseModel):
    blockchain: List[Block] = []

    # class Config:
    #     orm_mode = True


# post
class TransactionBase(BaseModel):
    recipient: str
    amount: float
