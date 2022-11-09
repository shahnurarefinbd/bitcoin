# Hash a single string with hashlib.sha256
from hashlib import sha256
import json
import os
# from server import send_transaction_file

transactions_file = os.getcwd() + '/transactions.json'


# Transaction Class, Taking input of Transaction
class Transaction:
    def __init__(self, timestamp, sender_address, receiver_address, amount, sign):
        self.timestamp = timestamp
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount
        self.sign = sign

    def getdata(self):
        transaction_data = {'timestamp': self.timestamp, 'from': self.sender_address, 'to': self.receiver_address,
                            'amount': self.amount, 'sign': self.sign}
        return transaction_data

    def send_money(self):
        current_transaction = self.getdata()
        a_string = json.dumps(current_transaction)

        # Hashing Transaction Data
        hashed_string = sha256(a_string.encode('utf-8')).hexdigest()

        print(hashed_string)

        new_transaction_file = os.getcwd() + "/transactions/" + hashed_string + '.json'
        # Hashed value saved in json file and create a new file using hash.
        with open(new_transaction_file, 'w') as f:
            f.write(a_string)

        current_transaction_file_size = os.path.getsize(transactions_file)
        print(current_transaction_file_size)
        if current_transaction_file_size > 0:
            f = open(transactions_file, "r")
            transactions = json.loads(f.read())
            f.close()
        else:
            transactions = []

        transaction_data = {'hash': hashed_string, 'content': current_transaction}
        transactions.append(transaction_data)
        f = open(transactions_file, "w")
        f.write(json.dumps(transactions))
        f.close()

        # send_transaction_file(new_transaction_file)
