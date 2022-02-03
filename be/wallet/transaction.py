# %%
from uuid import uuid4
from time import time_ns
from be.config import MINING_REWARD, MINING_REWARD_INPUT
from be.wallet.wallet import Wallet


class Transaction:
    """
    document of an exchange in currency from a sender to one or more recipients
    one transaction per sender per block
    """

    def __init__(
        self,
        sender_wallet=None,
        recipient=None,
        amount=None,
        id=None,
        output=None,
        input=None,
    ):
        # unique id for each transaction. prevents duplicate transactions
        # also helpful for searching
        self.id = id or str(uuid4())[:8]
        self.output = output or self.create_output(sender_wallet, recipient, amount)
        self.input = input or self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount):
        """
        structure of the output data for the transaction
        """
        if amount > sender_wallet.balance:
            raise Exception("Amount exceeds balance")

        output = {}
        output[recipient] = amount
        # the 'change' for the sender
        output[sender_wallet.address] = sender_wallet.balance - amount
        return output

    def create_input(self, sender_wallet, output):
        """
        structure input data for the transaction
        sign the transaction and include the sender's public key and address
        """
        return {
            "timestamp": time_ns(),
            "amount": sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(output),
        }

    def update(self, sender_wallet, recipient, amount):
        """
        update the transaction with an existing or new recipient
        """

        if amount > self.output[sender_wallet.address]:
            raise Exception("Amount exceeds balance")

        self.output[sender_wallet.address] -= amount

        if recipient in self.output:
            self.output[recipient] += amount
        else:
            self.output[recipient] = amount

        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        deserialize transaction from json
        """
        return Transaction(
            **transaction_json
            # id=transaction_json["id"],
            # input=transaction_json["input"],
            # output=transaction_json["output"],
        )

    @staticmethod
    def is_valid_transaction(transaction):
        """
        validate a transaction
        raise an exception for invalid transactions
        """
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception("Invalid mining reward")
            return

        output_total = sum(transaction.output.values())
        if transaction.input["amount"] != output_total:
            raise Exception("Invalid transaction output values")

        if not Wallet.verify(
            transaction.input["public_key"],
            transaction.output,
            transaction.input["signature"],
        ):
            raise Exception("Invalid signature")

    @staticmethod
    def reward_transaction(miner_wallet):
        """
        generate a reward transaction that awards the miner
        """
        output = {}
        output[miner_wallet.address] = MINING_REWARD
        return Transaction(input=MINING_REWARD_INPUT, output=output)


if __name__ == "__main__":
    transaction = Transaction(Wallet(), "recipient", 0)
    print(transaction.__dict__)
    print(transaction.__dict__ == transaction.from_json(transaction.to_json()).__dict__)

# %%
