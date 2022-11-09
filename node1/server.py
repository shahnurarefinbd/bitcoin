# from audioop import add
# from http import client, server
import hashlib
import json
import socket
import os
import threading
from datetime import time

import block

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on (non-privileged ports are > 1023)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
nodes = [5555, 5557]

block_chain = block.blockchain()


def find_hash(dict):
    hashvalue = hashlib.sha256(json.dumps(dict).encode('utf-8')).hexdigest()
    return hashvalue


def valid_block(block, previous_hash, proof):
    if block.get('previous_hash') == previous_hash and find_hash(block) == proof:
        return True
    return False


# to add more nodes  add in teh nodes array
def send_to_other_nodes(block):
    for peer in nodes:
        if peer != PORT:
            node_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            node_con.connect((HOST, peer))
            node_con.send('add_block'.encode('UTF-8'))
            message = node_con.recv(1024).decode('UTF-8')
            print(message)
            node_con.send(json.dumps(block).encode('UTF-8'))
            message = node_con.recv(1024).decode('UTF-8')
            node_con.close()


def handling_client(client, blockchain):
    while True:
        data = client.recv(1024).decode('UTF-8')
        if data == 'Mining':
            transactions_file = os.getcwd() + '/transactions.json'
            f = open(transactions_file, "r")
            transactions = json.loads(f.read())
            previous_block = blockchain.get_last_node()
            client.sendall(json.dumps(previous_block).encode('UTF-8'))
            proof = client.recv(1024).decode('UTF-8')
            client.send('reccived proof'.encode('UTF-8'))
            data = client.recv(7000)
            block = json.loads(data.decode('UTF-8'))
            if valid_block(block, blockchain.get_last_node().get('hash'), proof):
                block['hash'] = proof
                blockchain.chain.append(block)
                f = open("Blocks1/" + str(proof), 'w')
                f.write(json.dumps(block))
                f.close()
                send_to_other_nodes(block)
                client.send(('mined block' + str(len(blockchain.chain))).encode('UTF-8'))
            else:
                client.send('Already block mined'.encode('UTF-8'))
        if data == 'add_block':
            client.send('send block to add'.encode('UTF-8'))
            block = json.loads(client.recv(8000).decode('UTF-8'))
            blockchain.chain.append(block)
            with open("Blocks1/" + str(block.get('hash')), 'w') as f:
                f.write(json.dumps(block))
            f.close()
            client.send("success".encode('UTF-8'))


while True:
    clientsocket, address = s.accept()
    print("Connection From " + str(address) + "established. ")
    thread = threading.Thread(target=handling_client, args=(clientsocket, block_chain,))
    thread.start()
