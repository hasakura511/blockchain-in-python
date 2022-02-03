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


@router.get("/mine", response_model=Block)
def get_mined_block():
    try:
        block_json = db_get_mined_block()
        print(block_json)
    except Exception as e:
        # print(e)
        raise HTTPExceptions.unprocessable(str(e))
    return block_json
