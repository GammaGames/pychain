from flask import Flask, request, jsonify
from chain import Chain
import signal
import json

node = Flask(__name__)

blockchain = Chain()
my_transactions = []
peer_nodes = []
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"


def handle_sigint(signal, frame):
    """Save chain to archive on app quit
    """
    blockchain.save_archive()
    exit()


signal.signal(signal.SIGINT, handle_sigint)


@node.route("/transaction", methods=["POST"])
def transaction():
    """Add a new transaction
    Returns
        status : str
    """
    previous_len = len(my_transactions)
    new_transaction = request.get_json()
    my_transactions.append(new_transaction)
    print(f"{new_transaction['amount']} @ {new_transaction['from']} -> {new_transaction['to']}")
    return "Success" if len(my_transactions) > previous_len else "Failure"


@node.route("/mine", methods=["GET"])
def mine():
    """Sync chain, add mine transaction, and add block to chain
    Returns
        block : json
    """
    _consensus()
    my_transactions.append({
        "from": "network",
        "to": miner_address,
        "amount": 1
    })

    # Add current transactions to block
    new_data = {
        "transactions": list(my_transactions)
    }
    # Clear my transactions
    my_transactions[:] = []
    new_block = blockchain.add_block(new_data)
    return jsonify(new_block.get_data())


@node.route("/blocks", methods=["GET"])
def blocks():
    """Get list of blocks
    Returns
        blocks : json
    """
    return jsonify(blockchain.get_chain())


def _find_new_chains():
    """Get all peer chains
    """
    other_chains = []
    for url in peer_nodes:
        block = json.loads(request.request(f"{url}/blocks").content)
        other_chains.append(block)
    return other_chains


def _consensus():
    """Decide on common chain
    """
    global blockchain
    other_chains = _find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain


node.run()
