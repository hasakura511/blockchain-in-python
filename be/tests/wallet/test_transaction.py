import pytest
from be.wallet.transaction import Transaction
from be.wallet.wallet import Wallet
from be.config import MINING_REWARD, MINING_REWARD_INPUT, STARTING_BALANCE


def test_transaction():
    sender_wallet = Wallet()
    recipient = "recipient"
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)
    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert "timestamp" in transaction.input
    assert transaction.input["amount"] == sender_wallet.balance
    assert transaction.input["address"] == sender_wallet.address
    assert transaction.input["public_key"] == sender_wallet.public_key

    assert Wallet.verify(
        transaction.input["public_key"],
        transaction.output,
        transaction.input["signature"],
    )


def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match="Amount exceeds balance"):
        Transaction(Wallet(), "recipient", STARTING_BALANCE + 1)


def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, "recipient", 0)

    with pytest.raises(Exception, match="Amount exceeds balance"):
        transaction.update(sender_wallet, "new_recipient", STARTING_BALANCE + 1)


def test_transaction_update():
    sender_wallet = Wallet()
    recipient1 = "recipient1"
    amount1 = 50
    transaction = Transaction(sender_wallet, recipient1, amount1)

    recipient2 = "recipient2"
    amount2 = 20
    transaction.update(sender_wallet, recipient2, amount2)

    assert transaction.output[recipient2] == amount2
    assert (
        transaction.output[sender_wallet.address]
        == sender_wallet.balance - amount1 - amount2
    )
    assert Wallet.verify(
        transaction.input["public_key"],
        transaction.output,
        transaction.input["signature"],
    )

    transaction.update(sender_wallet, recipient1, amount2)
    assert transaction.output[recipient1] == amount1 + amount2
    assert (
        transaction.output[sender_wallet.address]
        == sender_wallet.balance - amount1 - amount2 - amount2
    )
    assert Wallet.verify(
        transaction.input["public_key"],
        transaction.output,
        transaction.input["signature"],
    )


def test_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), "recipient", 50))


def test_invalid_transaction():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, "recipient", 50)
    transaction.output[sender_wallet.address] = STARTING_BALANCE

    with pytest.raises(Exception, match="Invalid transaction output values"):
        Transaction.is_valid_transaction(transaction)

    transaction = Transaction(sender_wallet, "recipient", 50)
    # transaction is the same, but wallet id is different
    transaction.input["signature"] = Wallet().sign(transaction.output)
    with pytest.raises(Exception, match="Invalid signature"):
        Transaction.is_valid_transaction(transaction)


def test_transaction_serialization():
    transaction = Transaction(Wallet(), "recipient", 0)
    assert transaction.__dict__ == transaction.from_json(transaction.to_json()).__dict__


def test_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINING_REWARD


def test_valid_reward_transaction():
    reward_transaction = Transaction.reward_transaction(Wallet())
    Transaction.is_valid_transaction(reward_transaction)


def test_valid_reward_transaction_extra_recipient():
    reward_transaction = Transaction.reward_transaction(Wallet())
    reward_transaction.output["extra_recipient"] = 60

    with pytest.raises(Exception, match="Invalid mining reward"):
        Transaction.is_valid_transaction(reward_transaction)


def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    reward_transaction = Transaction.reward_transaction(miner_wallet)
    reward_transaction.output[miner_wallet] = 6000

    with pytest.raises(Exception, match="Invalid mining reward"):
        Transaction.is_valid_transaction(reward_transaction)
