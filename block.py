import hashlib


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce, num_zeroes):
        """A basic block, will create its hash on its own
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.num_zeroes = num_zeroes
        self.hash = self.hash_block()

    def get_data(self):
        """Get a dictionary representation of the block
        Returns
            data : dict
        """
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
        """Get hash for block
        Returns
            hash : str
        """
        sha = hashlib.sha256()
        block = f"{self.index}{self.timestamp}{self.data}" + \
            f"{self.previous_hash}{self.num_zeroes}{self.nonce}"
        sha.update(block.encode('utf-8'))
        return sha.hexdigest()
