import os
import json
import hashlib
import gzip
from datetime import datetime
from block import Block
from helper import proof_of_work


class Chain():
    # TODO segment blocks into size limited files
    def __init__(self, chain_name='chain'):
        """Load a chine from the file and validate
        """
        self.chain_name = chain_name
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.chainfile = os.path.join(dir_path, chain_name)
        self.archive_file = f"{self.chainfile}.gzip"
        self.text_file = f"{self.chainfile}.txt"

        if self._create_chain():
            self._create_genesis_block()
        self.validate_chain()
        self.data = []

    def save_archive(self):
        """Save chain to archive
        """
        with open(self.text_file, 'r') as src, gzip.open(self.archive_file, 'wt') as dest:
            dest.write(src.read())
        os.remove(self.text_file)

    def _create_chain(self):
        """Load gzip into text file if exists, else create text file
        Returns
            file_created : bool
        """
        if os.path.isfile(self.archive_file):
            with gzip.open(self.archive_file, 'rt') as src, open(self.text_file, 'w') as dest:
                dest.write(src.read())
            return False
        elif not os.path.isfile(self.text_file) or os.stat(self.text_file).st_size == 0:
            f = open(self.text_file, 'w')
            f.close()
            return True
        return False

    def _create_genesis_block(self):
        """Create a basic initial block
        """
        block = Block(
            0,
            str(datetime.now()),
            "Genesis block",
            '0',
            1,
            0
        )
        self._write_to_chain(block.get_data())

    def _write_to_chain(self, block):
        """Write a block to the chain
        """
        with open(self.text_file, 'a') as f:
            f.write(f"{json.dumps(block)}\n")

    def create_new_block(self):
        """Create a new block given the current chain's un-hashed data
        """
        with open(self.text_file, 'r') as f:
            previous_block = f.readlines()[-1]
            previous_block = json.loads(previous_block)

        index = previous_block['index'] + 1
        previous_hash = previous_block['hash']
        timestamp = str(datetime.now())
        nonce, num_zeroes = proof_of_work(previous_hash)

        self.block = Block(
            index,
            timestamp,
            self.data,
            previous_hash,
            nonce,
            num_zeroes
        )
        self._write_to_chain(self.block.get_data())
        self.data = []

    def add_data(self, data):
        """Add data to chain
        """
        self.data.append(data)

    def add_block(self, data):
        """Add block with data
        """
        self.add_data(data)
        self.create_new_block()
        return self.block

    def _return_hash(self, previous_hash, nonce):
        """Get hash with a previous hash and nonce
        Returns
            hash : str
        """
        sha = hashlib.sha256()
        sha.update(f"{previous_hash}{nonce}".encode('utf-8'))
        return sha.hexdigest()

    def _validate_hash(self, hash, num_zeroes):
        """Check if hash starts with num zeroes
        Returns
            valid : bool
        """
        if str(hash[:num_zeroes]) != "0" * num_zeroes:
            raise ValueError("Invalid chain")
        else:
            return True

    def validate_chain(self, chain=None):
        """Validate either current chain or the file passed in
        Returns
            valid : bool
        """
        num_genesis_blocks = 0

        if chain is None:
            chain = self.text_file

        # For each block in the file
        with open(chain, 'r') as f:
            for line in f:
                # Get basic variables to validate
                this_hash = None
                block_to_validate = json.loads(line)
                index = block_to_validate["index"]
                num_zeroes = block_to_validate["num_zeroes"]
                nonce = block_to_validate["nonce"]
                previous_hash = block_to_validate["previous_hash"]

                # Keep track of number of genesis blocks
                if index == 0:
                    num_genesis_blocks += 1
                # If hashes don't equal, chain is invalid
                else:
                    if this_hash is not None and this_hash != previous_hash:
                        raise ValueError("Invalid hashes, broken chain")

                # Validate hash
                this_hash = block_to_validate["hash"]
                hash_to_validate = self._return_hash(previous_hash, nonce)
                self._validate_hash(hash_to_validate, num_zeroes)

        if num_genesis_blocks > 1:
            raise ValueError("Multiple genesis blocks")

        return True

    def get_chain(self):
        """Get list of chain dicts
        Returns
            blocks : list(dict)
        """
        self.validate_chain()
        results = []

        with open(self.text_file, 'r') as f:
            for line in f:
                b = json.loads(line)
                b.pop("hash")
                block = Block(**b)
                results.append(block.get_data())

        return results


if __name__ == '__main__':
    """Debug function to create chain
    """
    b = Chain()
    b.add_data('this is some data!')
    b.add_data('this is also some data!')
    b.create_new_block()
    b.add_data('test data')
    b.create_new_block()
    b.validate_chain()
