# %%
from be.blockchain.block import Block
from be.wallet.transaction import Transaction
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from dotenv import load_dotenv
import os, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.environ["PN_SUBSCRIBE_KEY"]
pnconfig.publish_key = os.environ["PN_PUBLISH_KEY"]
pnconfig.uuid = os.environ["PN_UUID"]

# pubsub channels
CHANNELS = {"TEST": "TEST", "BLOCK": "BLOCK", "TRANSACTION": "TRANSACTION"}

# listens to the channel
class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        channel = message_object.channel
        message = message_object.message
        print(f"\n-- Channel: {channel} | Message: {message}")
        if channel == CHANNELS["BLOCK"]:
            # print(type(message))
            block = Block.from_json(message)
            # [:] creates a copy
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            # print(f"\n\npotential chain {len(potential_chain)}", potential_chain)
            # print(
            #     f"\n\self.blockchain.chain {len(self.blockchain.chain)}",
            #     self.blockchain.chain[:],
            # )
            # print(self.blockchain.chain == potential_chain)

            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
            except Exception as e:
                print(f"\n -- Did not replace chain: {e}")
        elif channel == CHANNELS["TRANSACTION"]:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print("\n -- Set new transaction in the transaction pool")


class PubSub:
    """
    Handles the pub/sub layer of the application
    provides communication between nodes of the blockchain networks
    """

    def __init__(self, blockchain, transaction_pool):
        print("subscribe_key", pnconfig.subscribe_key)
        print("publish_key", pnconfig.publish_key)
        self.pubsub = PubNub(pnconfig)
        # subscribe to test channel
        self.pubsub.subscribe().channels(CHANNELS.values()).execute()
        self.pubsub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        publish the message object to the channels
        """
        self.pubsub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block_json):
        """
        Broadcash a block object to all nodes
        """
        self.publish(CHANNELS["BLOCK"], block_json)

    def broadcast_transaction(self, transaction_json):
        """
        broadcast a transaction to all nodes
        """
        self.publish(CHANNELS["TRANSACTION"], transaction_json)


def main():
    pubsub = PubSub()
    time.sleep(1)
    # publish to test channel
    # The message can be anything as long as it consists of the basic data types like dictionaries lists numbers, strings bool etc.
    pubsub.publish(CHANNELS["TEST"], {"test": "test"})


# %%
if __name__ == "__main__":
    main()

# %%
