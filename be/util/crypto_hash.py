# %%
import hashlib
import json
from typing import List


def crypto_hash(*args: List[str]) -> hash:
    """
    return a sha-256 hash of the given data
    secure hash algorithm returning 256 bits or 64hex digits

    utf-8 of standard conversions for characters into an equivalent 8 bit representation a bit being a set of zeros and ones in binary.

    proper cryptohash needs to sort the arguments
    """
    stringified_data = "".join(sorted([json.dumps(arg) for arg in args]))
    # print(stringified_data)
    hash = hashlib.sha256(stringified_data.encode("utf-8")).hexdigest()
    # print(stringified_data, "->", len(hash), hash)
    return hash


if __name__ == "__main__":
    hash = crypto_hash(1)
    hash = crypto_hash(1)
    hash = crypto_hash("😱")
    hash1 = crypto_hash(
        {"json": [1, 2, 3, "asdfasdfasdfasdfasfasdfasf" * 64]}, 1, 2, "   🎊"
    )
    hash2 = crypto_hash(
        "   🎊", 1, 2, {"json": [1, 2, 3, "asdfasdfasdfasdfasfasdfasf" * 64]}
    )
    assert hash1 == hash2


# %%

# %%
