# %%
from time import time_ns
from be.util.crypto_hash import crypto_hash
from be.util.utils import timing, hex_to_binary
from be.config import MINE_RATE, INIT_DIFFICULTY
import json


class Block:
    # block: unit of storage

    def __init__(self, data, hash, last_hash, timestamp, difficulty, nonce):
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.last_hash = last_hash
        self.difficulty = difficulty
        self.nonce = nonce

    GENESIS_DATA = dict(
        data=[],
        last_hash=crypto_hash(0),
        timestamp=0,
        difficulty=INIT_DIFFICULTY,
        nonce=0,
    )
    GENESIS_DATA["hash"] = crypto_hash(*GENESIS_DATA)

    def __repr__(self):
        return (
            "Block("
            f"timestamp: {self.timestamp}, "
            f"last_hash: {self.last_hash}, "
            f"hash: {self.hash}, "
            f"data: {self.data}, "
            f"difficulty: {self.difficulty}, "
            f"nonce: {self.nonce}, "
            ")"
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    @timing
    def mine_block(cls, last_block, data):
        """
        mines a block based on given last_block and data, until a block hash
        is found that meets the leading 0's proof of work requirement
        """
        # nanoseconds since 1/1/1970
        timestamp = time_ns()
        last_hash = last_block.hash
        difficulty = cls.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        # hex_to_binary conversion leads to precise block mining times
        while hex_to_binary(hash)[0:difficulty] != "0" * difficulty:
            # ensures creation of new hash
            nonce += 1
            timestamp = time_ns()
            difficulty = cls.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(data, hash, last_hash, timestamp, difficulty, nonce)

    @classmethod
    def genesis(cls):
        """
        returns first block
        -genesis block needs to be static for all peers to sync

        """

        return Block(**cls.GENESIS_DATA)

    @staticmethod
    def verify_hash(block):
        hash_params = [block.__dict__[k] for k in block.__dict__.keys() if k != "hash"]
        hash = crypto_hash(*hash_params)
        if hash == block.hash:
            # print(f"block verified.")
            return True
        return False

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        calculate adjusted difficulty per mine rate
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if last_block.difficulty - 1 > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate the block by enforcing the following rules:
        1. the block must have the proper last_hash reference
        2. the block must meet the proof of work requirement
        3. the difficulty must only adjust by one
        4. the block hash must be a valid combination of the block fields
        """
        if last_block.hash != block.last_hash:
            raise Exception("last_block.hash != block.last_hash")

        if hex_to_binary(block.hash)[: block.difficulty] != "0" * block.difficulty:
            raise Exception(
                f"hash {hex_to_binary(block.hash)} does not have {block.difficulty} 0's"
            )

        if abs(block.difficulty - last_block.difficulty) > 1:
            raise Exception(
                f"difficulty adjustment {abs(block.difficulty - last_block.difficulty)} > 1"
            )

        # assert block.__dict__.keys() == last_block.__dict__.keys()
        if not Block.verify_hash(block):
            raise Exception("reconstructed has does not equal block hash")

    def to_json(self):
        """
        serialize block
        """
        # block_json = self.__dict__.copy()
        # block_json["data"] = json.dumps(block_json)
        return self.__dict__

    @staticmethod
    def from_json(block_json):
        """
        deserialize block's json representation back into a block json
        """
        return Block(**block_json)


if __name__ == "__main__":
    print(f"__name__: {__name__}")
    # b = Block("data", "hash", "last_hash", "timestamp",)
    # print(b.GENESIS_DATA)
    # print(b)
    genesis_block = Block.genesis()
    new_block = Block.mine_block(genesis_block, "new block")
    print(new_block)
    Block.verify_hash(new_block)
    # new_block.last_hash = "corrupted data"
    # new_block.difficulty = 500
    # new_block.new_field = 123
    Block.is_valid_block(genesis_block, new_block)
# %%
