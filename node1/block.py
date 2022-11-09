import hashlib
import os
import time
import json


# from server import send_blockchain
def find_hash(dict):
    hashvalue = hashlib.sha256(json.dumps(dict, sort_keys=True).encode('utf-8')).hexdigest()
    return hashvalue


class blockchain:
    def __init__(self):
        self.chain = []
        first_block = {'transactions': [], 'timestamp': 0, 'previous_hash': "NA", 'height': 0}
        hash_value = find_hash(first_block)
        first_block['hash'] = hash_value
        self.chain.append(first_block)

    def get_last_node(self):
        return self.chain[-1]
