from fastapi import APIRouter, Depends
from be.routes.schemas import TransactionBase, Wallet
from be.db.db_bc import db_post_wallet_transaction
from be.routes.exceptions import HTTPExceptions
from be.db.db_bc import wallet

# from sqlalchemy.orm import Session
# from db.db_user import *
# from db.databases import get_db
from typing import List


router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.post("/transact")
def post_wallet_transaction(transaction: TransactionBase):
    try:
        tx_json = db_post_wallet_transaction(transaction)
    except Exception as e:
        # print(e)
        raise HTTPExceptions.unprocessable(str(e))

    return tx_json


@router.get("/info", response_model=Wallet)
def get_wallet_info():
    return wallet.to_json()
