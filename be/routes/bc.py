from fastapi import APIRouter, Depends
from be.routes.schemas import Block, Blockchain
from be.db.db_bc import *
from be.routes.exceptions import HTTPExceptions


# from sqlalchemy.orm import Session
# from db.db_user import *
# from db.databases import get_db
from typing import List

router = APIRouter(prefix="/bc", tags=["bc"])


@router.get("", response_model=List[Block])
def get_blockchain():
    try:
        bc_json = db_get_blockchain()
    except Exception as e:
        # print(e)
        raise HTTPExceptions.unprocessable(str(e))
    return bc_json


@router.get("/range", response_model=List[Block])
def get_blockchain_range(start: int, end: int | None = None):
    # print(start, end)
    try:
        bc_json = db_get_blockchain()
    except Exception as e:
        # print(e)
        raise HTTPExceptions.unprocessable(str(e))
    return bc_json[::-1][start:end]


@router.get("/length", response_model=int)
def get_blockchain_length():
    try:
        bc_length = len(db_get_blockchain())
    except Exception as e:
        # print(e)
        raise HTTPExceptions.unprocessable(str(e))
    return bc_length


@router.get("/mine", response_model=Block)
def get_mined_block():
    try:
        block_json = db_get_mined_block()
        # print(block_json)
    except Exception as e:
        # print(e)
        raise HTTPExceptions.unprocessable(str(e))
    return block_json


@router.get("/known-addresses", response_model=List[str])
def get_known_addresses():
    known_addresses = set()
    bc = db_get_blockchain()
    # print(bc)
    for b in bc:
        for tx in b["data"]:
            known_addresses.update(tx["output"].keys())

    return known_addresses


@router.get("/transactions", response_model=List[dict])
def get_transactions():
    transactions = transaction_pool.transaction_data()
    # print(transactions)
    return transactions
