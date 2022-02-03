from be.blockchain.blockchain import Blockchain
from time import time_ns
from be.config import SECONDS

bc = Blockchain()

times = []

for i in range(1000):
    start_time = time_ns()
    bc.add_block(i)
    end_time = time_ns()

    mining_time = (end_time - start_time) / SECONDS
    times.append(mining_time)

    avg_time = sum(times) / len(times)
    print(i)
    print(f"new block difficulty: {bc.chain[-1].difficulty}")
    print(f"mining_time: {mining_time}")
    print(f"avg time: {avg_time}")

