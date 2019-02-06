import hashlib


def proof_of_work(previous_hash, num_zeroes=5):
    """
    Uses `previous_hash` to solve for a `nonce`, where the resulting
        hash starts with a number of zero bits ( number_of_zeroes ).
    Returns
        nonce : int
    """
    nonce = None
    incrementor = 0
    leading_zeroes = '0' * num_zeroes
    while not nonce:
        sha = hashlib.sha256()
        sha.update(f"{previous_hash}{incrementor}".encode('utf-8'))
        challenge_hash = sha.hexdigest()
        if str(challenge_hash[:num_zeroes]) == leading_zeroes:
            nonce = incrementor
        else:
            incrementor += 1
    return nonce, num_zeroes
