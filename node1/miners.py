import hashlib
import os
import json
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
import ledger

# Declaring Block file path
block_file = os.getcwd() + "/blockchain.json"


MAX_NONCE = 100000000000


def verify_message(message, pub_key, signature):
    public_key = load_pem_public_key(pub_key, default_backend())
    try:
        valid = False
        balance = ledger.query_balance(message['signer'])
        valid_public_key = public_key.verify(
            signature,
            json.dumps(message).encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        if int(message['amount']) < balance:
            print('have sufficient balance')
            valid = True

        return valid
    except InvalidSignature as e:
        print("Invalid Signature")
        return False








