# %%
from be.blockchain.block import Block
import time
from be.config import MINE_RATE, SECONDS
from be.util.utils import hex_to_binary
import pytest
from copy import deepcopy


def test_mine_block():
    last_block = Block.genesis()
    data = "test-data"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0 : block.difficulty] == "0" * block.difficulty


def test_quickly_mined_block():
    first_block = Block.mine_block(Block.genesis(), "test")
    second_block = Block.mine_block(first_block, "test2")
    assert first_block.difficulty + 1 == second_block.difficulty


def test_slowly_mined_block():
    first_block = Block.mine_block(Block.genesis(), "test")
    time.sleep(MINE_RATE / SECONDS)
    second_block = Block.mine_block(first_block, "test2")
    assert first_block.difficulty - 1 == second_block.difficulty


def test_mined_block_difficulty_ge_1():
    first_block = Block.mine_block(Block.genesis(), "test")
    first_block.difficulty = 1
    # print(first_block)
    time.sleep(MINE_RATE / SECONDS)
    second_block = Block.mine_block(first_block, "test2")
    assert second_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()


# pytest looks for functions with the same name, e.g. 'last_block' declaredabove
@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, "new block")


def test_genesis(last_block):
    # genesis = Block.genesis()

    assert isinstance(last_block, Block)
    # assert last_block.last_hash == last_block.GENESIS_DATA["hash"]
    # assert last_block.data == last_block.GENESIS_DATA["data"]

    # assert str(last_block) == str(
    #     Block.mine_block(Block(**Block.GENESIS_DATA), Block.GENESIS_DATA["data"])
    # )
    for k, v in last_block.GENESIS_DATA.items():
        if "hash" not in k:
            assert getattr(last_block, k) == v


def test_is_valid_block(last_block, block):
    # genesis_block = Block.genesis()
    # new_block = Block.mine_block(genesis_block, "new block")
    # new_block.last_hash = "corrupted data"
    # new_block.difficulty = 500
    # genesis_block.difficulty = 0
    # new_block.new_field = 123
    Block.is_valid_block(last_block, block)


def test_is_not_valid_lasthash(last_block, block):
    block.last_hash = "corrupted data"
    with pytest.raises(Exception, match="last_block.hash != block.last_hash"):
        Block.is_valid_block(last_block, block)


def test_is_not_valid_difficulty_hash(last_block, block):
    block.difficulty = 500
    # block.hash = "0" + block.hash
    with pytest.raises(
        Exception,
        match=f"hash {hex_to_binary(block.hash)} does not have {block.difficulty} 0's",
    ):

        Block.is_valid_block(last_block, block)


def test_is_not_valid_difficulty_adjustment(last_block, block):
    last_block.difficulty = 0
    with pytest.raises(
        Exception,
        match=f"difficulty adjustment {abs(block.difficulty - last_block.difficulty)} > 1",
    ):
        Block.is_valid_block(last_block, block)


def test_is_not_valid_hash_fields(last_block, block):
    block.new_field = 123
    with pytest.raises(Exception, match="reconstructed has does not equal block hash"):
        Block.is_valid_block(last_block, block)
