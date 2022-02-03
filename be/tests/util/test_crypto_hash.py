from be.util.crypto_hash import crypto_hash


def test_crypto_hash():
    # test sorting
    assert crypto_hash(1, [2], "three") == crypto_hash("three", 1, [2])
    assert (
        crypto_hash("asdf")
        == "af35e58e9758cc7ef65ad6d81c5b8a7c9cfeb1645a31d4dfc741cc0e107ec08e"
    )

