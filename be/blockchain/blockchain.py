# %%
from be.blockchain.block import Block
from be.config import MINING_REWARD_INPUT
from be.wallet.transaction import Transaction
from be.wallet.wallet import Wallet


def lightning(data):
    return data + "*"


class Blockchain:
    # blockchain: public ledger of transactions

    def __init__(self):
        # genesis = Block("gen_data", "gen_hash", "gen_last_hash")
        self.chain = [Block.genesis()]

    def __repr__(self):
        # blockchain_str = "\n".join([str(x) for x in self.chain])
        # return blockchain_str
        return f"{self.chain}"

    def __iter__(self):
        # the yield statement suspends a function's execution and sends a value back to the caller
        # it retains enough sstate to enable function to ressume where it is left off
        for i in range(len(self.chain)):
            yield self.chain[i]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following applies:
        1. The incoming chain is longer than the local one.
        2. The incoming chain is formatted properly.
        """
        # print(f"\n\nincoming {len(chain)}", chain)
        # print(f"\n\nexisting {len(self.chain)}", self.chain)

        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace chain: incoming chain must be longer")

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Invalid chain: {e}")

        self.chain = chain
        print(f"\n -- Successfully replaced chain")

    def add_block(self, data):
        # last_block = self.chain[-1]
        # last_hash = self.chain[-1].hash
        # hash = lightning(f"{data} + {last_hash}")
        # block = Block(data, hash, last_hash)
        new_block = Block.mine_block(self.chain[-1], data)
        self.chain.append(new_block)

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain
        1. the chain must start with the genesis block
        2. blocks must be formatted correctly
        """
        # genesis test at test_genesis() in tests.test_block
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    def to_json(self):
        """
        serialize the blockchain into list of dicts
        """
        serialized_chain = [b.to_json() for b in self.chain]
        return serialized_chain

    @staticmethod
    def from_json(chain_json):
        """
        deserialize a list of serialized blocks into Blockchain instance
        The result will contain a chain list of block instances
        """
        blockchain = Blockchain()
        blockchain.chain = [Block(**d) for d in chain_json]
        Blockchain.is_valid_chain(blockchain.chain)
        return blockchain

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        enforces the rules of a chain composed of blocks of transactions
            -each transactionmust only appear once in the chain
            -there can only be one mining reward per block
            -each transaction must be valid
        """
        transaction_ids = set()

        for i, block in enumerate(chain):
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception("Transaction{transaction.id} is not unique")

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            f"There can only be one mining reward per block. Check block hash {block.hash}"
                        )

                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain, transaction.input["address"]
                    )
                    if historic_balance != transaction.input["amount"]:
                        raise Exception(
                            f"Transaction has an invalid input amount {transaction.id}"
                        )

                Transaction.is_valid_transaction(transaction)


if __name__ == "__main__":
    bc = Blockchain()
    bc.add_block("one")
    bc.add_block("two")
    bc.add_block("three")
    bc.add_block("four")
    bc.add_block("five")

    for i, b in enumerate(bc):
        print(i, b)

    print(bc)
    print(f"__name__: {__name__}")


# %%
