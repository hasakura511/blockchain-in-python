from be.blockchain.blockchain import Blockchain
from be.config import STARTING_BALANCE
from be.wallet.transaction import Transaction
from be.wallet.wallet import Wallet


def test_verify_valid_signature():
    data = {"test": "test"}
    wallet = Wallet()
    sig = wallet.sign(data)
    assert Wallet.verify(wallet.public_key, data, sig)


def test_verify_invalid_signature():
    data = {"test": "test"}
    wallet = Wallet()
    sig = wallet.sign(data)
    assert not Wallet.verify(Wallet().public_key, data, sig)
    assert not Wallet.verify(wallet.public_key, {}, sig)


def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE

    amount = 50
    transaction = Transaction(wallet, "recipient", amount)
    blockchain.add_block([transaction.to_json()])
    assert (
        Wallet.calculate_balance(blockchain, wallet.address)
        == STARTING_BALANCE - amount
    )

    received_amt_1 = 25
    received_tx_1 = Transaction(Wallet(), wallet.address, received_amt_1)

    received_amt_2 = 43
    received_tx_2 = Transaction(Wallet(), wallet.address, received_amt_2)

    blockchain.add_block([received_tx_1.to_json(), received_tx_2.to_json()])
    assert (
        Wallet.calculate_balance(blockchain, wallet.address)
        == STARTING_BALANCE - amount + received_amt_1 + received_amt_2
    )
