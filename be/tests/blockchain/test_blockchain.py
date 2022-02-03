import pytest
from be.blockchain.blockchain import Blockchain
from be.blockchain.block import Block
from be.wallet.transaction import Transaction
from be.wallet.wallet import Wallet


def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == Block.GENESIS_DATA["hash"]


@pytest.fixture
def test_data():
    # create blocks
    return [[Transaction(Wallet(), "recipient", amt).to_json()] for amt in range(1, 4)]


@pytest.fixture
def test_blockchain(test_data):
    blockchain = Blockchain()
    for block in test_data:
        blockchain.add_block(block)
    return blockchain


def test_add_block(test_blockchain, test_data):
    for i, b in enumerate(test_blockchain):
        # print(i, b)
        if i == 0:
            # genesis
            assert Block.GENESIS_DATA["data"] == b.data
            continue
        assert b.data == test_data[i - 1]


def tests_is_valid_chain(test_blockchain):
    Blockchain.is_valid_chain(test_blockchain.chain)


def test_replace_chain(test_blockchain):
    blockchain = Blockchain()
    blockchain.replace_chain(test_blockchain.chain)

    assert blockchain.chain == test_blockchain.chain


def test_replace_chain_shorter(test_blockchain):
    blockchain = Blockchain()
    with pytest.raises(
        Exception, match="Cannot replace chain: incoming chain must be longer"
    ):
        test_blockchain.replace_chain(blockchain.chain)


def test_replace_chain_shorter(test_blockchain):
    blockchain = Blockchain()
    test_blockchain.chain[1].hash = "bad hash"
    with pytest.raises(Exception, match=f"Invalid chain:"):
        blockchain.replace_chain(test_blockchain.chain)


def test_is_valid_transaction_chain(test_blockchain):
    # print(test_blockchain.chain)
    Blockchain.is_valid_transaction_chain(test_blockchain.chain)


def test_is_valid_transaction_chain_duplicate_tx(test_blockchain):
    transaction = Transaction(Wallet(), "recipient", 1).to_json()
    test_blockchain.add_block([transaction, transaction])

    with pytest.raises(Exception, match="is not unique"):
        Blockchain.is_valid_transaction_chain(test_blockchain.chain)


def test_is_valid_transaction_chain_multiple_rewards(test_blockchain):
    reward_1 = Transaction.reward_transaction(Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(Wallet()).to_json()

    test_blockchain.add_block([reward_1, reward_2])

    with pytest.raises(Exception, match="one mining reward per block"):
        Blockchain.is_valid_transaction_chain(test_blockchain.chain)


def test_is_valid_transaction_chain_bad_transaction(test_blockchain):
    bad_transaction = Transaction(Wallet(), "recipient", 1)
    bad_transaction.input["signature"] = Wallet().sign(bad_transaction.output)
    test_blockchain.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(test_blockchain.chain)


def test_is_valid_transaction_chain_bad_historic_balance(test_blockchain):
    wallet = Wallet()
    bad_transaction = Transaction(wallet, "recipient", 1)
    bad_transaction.output[wallet.address] = 9000
    bad_transaction.input["amount"] = 9001
    bad_transaction.input["signature"] = wallet.sign(bad_transaction.output)
    test_blockchain.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception, match="has an invalid input amount"):
        Blockchain.is_valid_transaction_chain(test_blockchain.chain)
