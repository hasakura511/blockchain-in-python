#%%
from functools import wraps
from time import time
from be.util.crypto_hash import crypto_hash


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"func:{f.__name__} took: {te-ts:2.4f} sec")
        return result

    return wrap


HEX_TO_BINARY_CONVERSION_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "a": "1010",
    "b": "1011",
    "c": "1100",
    "d": "1101",
    "e": "1110",
    "f": "1111",
}


def hex_to_binary(hex_string):
    binary_string = ""
    for char in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[char]
    # print(binary_string)
    return binary_string


if __name__ == "__main__":
    number = 451
    # remove 0x hex prefix -> 64 digit hex number
    hex_number = hex(number)[2:]
    bin_number = hex_to_binary(hex_number)
    print(f"hex_number: {hex_number}")
    print(f"hex_to_binary: {bin_number}")
    print(f"bin_to_decimal: {int(bin_number,2)}")

    binary_crypto_hash = hex_to_binary(crypto_hash("asdf"))
    print(f"binary_crypto_hash ({len(binary_crypto_hash)}): {binary_crypto_hash}")
# %%

