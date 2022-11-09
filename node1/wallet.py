import hashlib
import os
import json
import time
from datetime import datetime
from hashlib import sha256
import socket

import ledger
import keymanager
import miners
from transaction import Transaction

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5555))


def find_hash(dict):
    hashvalue = hashlib.sha256(json.dumps(dict).encode('utf-8')).hexdigest()
    return hashvalue


def calculate_proof(block_obj):
    difficulty = 3
    block_obj["nonce"] = 0
    hash_computed = find_hash(block_obj)
    while not hash_computed.startswith('0' * difficulty):
        block_obj["nonce"] += 1
        hash_computed = find_hash(block_obj)
    return hash_computed


# Displaying Menu to Select action
def menuDisplay():
    print("Please select from the followings")
    print("1: Check your balance")
    print("2: Sent Money to Another Users")
    print("3. Mine the block")
    print("4: Quit")
    response = input(">>>")
    return response


# Creating private Keys for new users
user_name = input("enter your username: ")
user_password = input("enter your password: ")

if os.path.exists("myPrivateKey/" + user_name + ".pem"):
    private_key = keymanager.load_private_key(user_name, user_password)
    if private_key is None:
        print("Password Error. Try Again")
        exit()
else:
    private_key = keymanager.create_new_key(user_name, user_password)

balance = ledger.query_balance(user_name)

if balance == 0:
    ledger.initiate_users(user_name)
else:
    pass

shouldContinue = True

while shouldContinue:
    response = menuDisplay()

    if response == "4":
        shouldContinue = False
    if response == "1":
        balance = ledger.query_balance(user_name)
        print("Username: ", user_name)
        print("Balance: ", balance)
    elif response == "2":
        to_user = input("Who do you want to send to? : ")
        amount = input("How much do you to sent? : $")

        value = {"name": to_user, "amount": amount, "signer": user_name}
        content = {"value": value}

        json_content = json.dumps(value)
        signature = keymanager.sign_message(json_content.encode('utf-8'), private_key)
        content["signature"] = signature.hex()

        sig_bytes = bytes.fromhex(content['signature'])

        f = open("pubkeys/" + user_name, "rb")
        pub_key = f.read()
        f.close()

        if miners.verify_message(value, pub_key, sig_bytes):
            ledger.transfer_value(user_name, to_user, amount)

            # Assigning Transaction Data to blockchain
            t = Transaction(time.time(), user_name, to_user, amount, content['signature'])
            t.send_money()


        else:
            print("verification fail")
    elif response == '3':
        transactions_file = os.getcwd() + '/transactions.json'
        f = open(transactions_file, "r")
        transactions = json.loads(f.read())
        f.close()

        if len(transactions) > 0:
            transactions.append(
                {'From_Adrress': 'Coinbase', 'To_adress': user_name, 'Amount': 100, 'Timestamp': time.time()})
            new_hash = sha256(json.dumps(transactions).encode('utf-8')).hexdigest()
            s.send('Mining'.encode('UTF-8'))
            previous_block = json.loads(s.recv(7000).decode('UTF-8'))
            Block = {'height': int(previous_block.get('height')) +1, 'previous_hash': previous_block.get('hash'),
                     'timestamp': time.time(),
                     'transactions': transactions}

            proof = calculate_proof(Block)
            s.send(proof.encode('UTF-8'))
            msg = s.recv(1024).decode('UTF-8')
            s.send(json.dumps(Block).encode('UTF-8'))
            message = s.recv(1024).decode('UTF-8')
            print(message)
            transactions = []
            f = open(transactions_file, "w")
            f.write(json.dumps(transactions))
            f.close()


        else:
            print("no transactions to mine")
    else:
        pass
