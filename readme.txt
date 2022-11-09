We have used macbook intel processor to run this program however it didn't work on MacBook Pro M1. 

Please create two folders inside node1 before executing program, because due to security purpose, I have deleted both : 
1. myPrivateKey
2. pubkeys


Note :

1. wallet.py is responsible of doing transaction. 
2. transaction folder will store all transaction by wallet and temporarily store transaction information in transaction.json
3. Another two folders myPrivateKey and pubkeys are used to store private keys and public keys of created users.
4. Ledger.py Calculates all the transaction and stored in Ledger.txt files.
5. keymanager.py files create private key, public key and verifies and sign each time user sends crypto to others.



Steps to add transactions and mine :

1) start server.py (runs at port 5555) and server2.py (runs at port 5557)
2) now start the wallets.py to do the transactions. Add any number of wallets.
3) Add transactions by selecting choice 2
4) To mine the block select choice 3
5) If the proof of work puzzle is solved, then the block is successfully mined and sent to other nodes.
6) Blockchain related to the server is seen at Blocks1 folder and Blockchain related to server2 is seen at Blocks2 folder.
7) Please exit the wallets to see all the blocks at servers.




