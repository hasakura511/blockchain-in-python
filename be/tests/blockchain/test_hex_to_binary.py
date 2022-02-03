from be.util.utils import hex_to_binary, crypto_hash


def test_hex_to_binary():
    number = 451
    # remove 0x hex prefix -> 64 digit hex number
    hex_number = hex(number)[2:]
    bin_number = hex_to_binary(hex_number)
    print(f"hex_number: {hex_number}")
    print(f"hex_to_binary: {bin_number}")
    print(f"bin_to_decimal: {int(bin_number,2)}")

    binary_crypto_hash = hex_to_binary(crypto_hash(number))
    print(f"binary_crypto_hash ({len(binary_crypto_hash)}): {binary_crypto_hash}")
    assert len(binary_crypto_hash) == 256
    assert number == int(bin_number, 2)

