from be.blockchain.blockchain import Blockchain
from be.wallet.transaction_pool import TransactionPool
from be.wallet.transaction import Transaction
from be.wallet.wallet import Wallet


def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), "recipient", 1)
    transaction_pool.set_transaction(transaction)
    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_clear_block_transaction():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), "recipient1", 1)
    transaction_2 = Transaction(Wallet(), "recipient1", 2)
    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)

    blockchain = Blockchain()
    blockchain.add_block([transaction_1.to_json(), transaction_2.to_json()])
    assert transaction_1.id in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transactions(blockchain)
    assert transaction_1.id not in transaction_pool.transaction_map
    assert transaction_2.id not in transaction_pool.transaction_map
