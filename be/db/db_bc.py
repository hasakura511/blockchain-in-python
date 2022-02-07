import os, requests, random
from be.blockchain.blockchain import Blockchain
from be.pubsub import PubSub
from be.config import ROOT_PORT
from be.wallet.wallet import Wallet
from be.wallet.transaction import Transaction
from be.wallet.transaction_pool import TransactionPool

blockchain = Blockchain()
# print(blockchain.chain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)
wallet = Wallet(blockchain)
ACTIVE_PEERS = []


def initialize_peer():
    try:
        result = requests.get(f"http://localhost:{ROOT_PORT}/bc")
        # print("root_result: ", result, result.json())
        result_chain = Blockchain.from_json(result.json()).chain
        blockchain.replace_chain(result_chain)
    except Exception as e:
        print(f"\n -- Did not replace chain: {e}")

    # return peer port
    if ACTIVE_PEERS:
        ACTIVE_PEERS.append(ACTIVE_PEERS[-1] + 1)
    else:
        ACTIVE_PEERS.append(ROOT_PORT + 1)

    return ACTIVE_PEERS[-1]


def db_get_blockchain():
    # for i in range(3):
    #     blockchain.add_block(i)
    return blockchain.to_json()


def db_get_mined_block():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())

    blockchain.add_block(transaction_data)
    block_json = blockchain.chain[-1].to_json()
    pubsub.broadcast_block(block_json)
    transaction_pool.clear_blockchain_transactions(blockchain)
    return block_json


def db_post_wallet_transaction(transaction_base):
    recipient, amount = transaction_base.recipient, transaction_base.amount

    # check if there is an existing transaction in the pool
    existing_tx = transaction_pool.existing_transaction(wallet.address)
    if existing_tx:
        existing_tx.update(wallet, recipient, amount)
        tx_json = existing_tx.to_json()
    else:
        tx_json = Transaction(wallet, recipient, amount).to_json()

    pubsub.broadcast_transaction(tx_json)
    return tx_json


def seed_data():

    print("SEEDING DATA")
    for i in range(10):
        blockchain.add_block(
            [
                Transaction(
                    Wallet(), Wallet().address, random.randint(1, 50)
                ).to_json(),
                Transaction(
                    Wallet(), Wallet().address, random.randint(1, 50)
                ).to_json(),
            ]
        )


def seed_transaction_pool():
    print("SEEDING TRANSACTION POOL")
    for i in range(3):
        transaction_pool.set_transaction(
            Transaction(Wallet(), Wallet().address, random.randint(1, 50))
        )
