import hashlib
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce, num_zeroes, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.num_zeroes = num_zeroes
        self.hash = self.hash_block()

    def __str__(self):
        return f"\nINDEX: {self.index}\nDATA:  {self.data}\nHASH:  {self.hash}"

    def get_data(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "nonce": self.nonce,
            "num_zeroes": self.num_zeroes,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    def hash_block(self):
        sha = hashlib.sha256()
        block = f"{self.index}{self.timestamp}{self.data}" + \
            f"{self.previous_hash}{self.num_zeroes}{self.nonce}"
        sha.update(block.encode('utf-8'))
        return sha.hexdigest()




# def next_block(last_block):
#     new_index = last_block.index + 1
#     new_timestamp = datetime.now()
#     new_data = f"Block ID {new_index}"
#     last_hash = last_block.hash
#     return Block(new_index, new_timestamp, new_data, last_hash)

# def main():
#     blockchain = [create_genesis_block()]
#     previous_block = blockchain[0]
#     for index in range(0, 20):
#         new_block = next_block(previous_block)
#         blockchain.append(new_block)
#         previous_block = new_block
#         print(new_block)

# if __name__ == "__main__":
#     main()
