# %%
import json
from uuid import uuid4
from be.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature,
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

# uuid4 - unique string of 36 characters random, partially based on timestamp. unique across all projects


class Wallet:
    """
    An individual wallet for a miner
    keeps track of the miner's balance.
    allows a miner to authorize transactions
    """

    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        # three trillion possibilities for 8 characters
        self.address = str(uuid4())[:8]
        # self.balance = STARTING_BALANCE
        # bitcoin uses 256-bit elliptic cryptography
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.serialize_public_key()

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, json_data):
        """
        generate a signature based on the data using the local private keys
        private key + data => signature
        """
        # data must be bytes-like
        byte_data = json.dumps(json_data).encode("utf-8")
        # print(data)
        # elliptic cryptography digital signature algorithm
        signature = self.private_key.sign(byte_data, ec.ECDSA(hashes.SHA256()))
        return decode_dss_signature(signature)

    def serialize_public_key(self):
        """
        serialize the public key
        """
        public_key = self.private_key.public_key()
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    def to_json(self):
        return {
            "address": self.address,
            "balance": self.balance,
        }

    @staticmethod
    def deserialize_public_key(serialized_public_key):
        return serialization.load_pem_public_key(
            serialized_public_key.encode("utf-8"), default_backend()
        )

    @staticmethod
    def verify(public_key, json_data, signature):
        """
        verify signature
        public key + signature => verified
        public key + wrong signature  => unverified
        """
        deserialize_public_key = Wallet().deserialize_public_key(public_key)
        byte_data = json.dumps(json_data).encode("utf-8")
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcf in position 6: invalid continuation byte -->encode_dss_signature(r,s)
        signature = encode_dss_signature(signature[0], signature[1])
        try:
            deserialize_public_key.verify(
                signature, byte_data, ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def calculate_balance(blockchain, address):
        """
        calculate the balance of the given address given transactions in the blockchain.

        the balance is calculated by adding the output values that belong to the address since the most recent transaction by that address
        """

        balance = STARTING_BALANCE
        if not blockchain:
            return balance

        for block in blockchain.chain:
            for tx in block.data:
                if tx["input"]["address"] == address:
                    #  a new input transaction, balance is overwritten by the change
                    balance = tx["output"][address]
                elif address in tx["output"]:
                    balance += tx["output"][address]
        return balance


if __name__ == "__main__":
    wallet = Wallet()
    print(wallet.__dict__)
    data = {"test": "test"}
    sig = wallet.sign(data)
    print("sig", sig)
    print("valid sig", Wallet.verify(wallet.public_key, data, sig))
    print("valid sig", Wallet.verify(Wallet().public_key, data, sig))


# %%
