# %%
import requests, sys
from be.config import ROOT_PORT
from be.wallet.wallet import Wallet
from time import sleep
import json


def pp(func):
    def inner(*args, **kwargs):
        return json.dumps(func(*args, **kwargs), indent=2, sort_keys=True)

    return inner


PORT = ROOT_PORT

BASE_URL = f"http://localhost:{PORT}"


@pp
def get_blockchain():
    return requests.get(f"{BASE_URL}/bc").json()


@pp
def get_blockchain_mine():
    sleep(1)
    return requests.get(f"{BASE_URL}/bc/mine").json()


@pp
def post_wallet_transact(recipient, amount):
    return requests.post(
        f"{BASE_URL}/wallet/transact",
        json={"recipient": recipient, "amount": amount},
    ).json()


@pp
def get_wallet_info():
    return requests.get(f"{BASE_URL}/wallet/info").json()


start_blockchain = get_blockchain()
print("\nstart_blockchain:", start_blockchain)

recipient = Wallet().address

post_wallet_transact_1 = post_wallet_transact(recipient, 21)
print(f"\npost_wallet_transact_1: {post_wallet_transact_1}")

sleep(1)
post_wallet_transact_2 = post_wallet_transact(recipient, 21)
print(f"\npost_wallet_transact_2: {post_wallet_transact_2}")

mined_block = get_blockchain_mine()
print(f"\nmined_block: {mined_block}")


wallet_info = get_wallet_info()
print(f"\nwallet_info: {wallet_info}")
# %%

print(sys.argv)
