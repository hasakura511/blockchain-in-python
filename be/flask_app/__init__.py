import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("appending", BASE_DIR)
sys.path.append(BASE_DIR)

from flask import Flask, jsonify
from be.blockchain.blockchain import Blockchain
from be.pubsub import PubSub
import random
import requests


app = Flask(__name__)
blockchain = Blockchain()
# print(blockchain.chain)
pubsub = PubSub(blockchain)


@app.route("/")
def index():
    return "Flask Blockchain Index"


@app.route("/bc")
def route_blockchain():
    # for i in range(3):
    #     blockchain.add_block(i)
    return jsonify(blockchain.to_json())


@app.route("/bc/mine")
def route_blockchain_mine():
    transaction_data = "stubbed_transaction_data"
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1].__dict__
    pubsub.broadcast_block(block)
    return jsonify(block)


PORT = ROOT_PORT = 5555
if os.environ.get("PEER"):
    print("PEER MODE")
    PORT = random.randint(5556, 6000)
    result = requests.get(f"http://localhost:{ROOT_PORT}/bc")
    # print("root_result: ", result, result.json())
    result_chain = Blockchain.from_json(result.json()).chain

    try:
        blockchain.replace_chain(result_chain)
    except Exception as e:
        print(f"\n -- Did not replace chain: {e}")

# print(PORT)
app.run(port=PORT)
