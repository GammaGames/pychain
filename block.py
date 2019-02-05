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
