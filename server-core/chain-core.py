import hashlib
import time
import json
from uuid import uuid4
from flask import Flask,jsonify,request
import requests

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.cur_transactions = []
        self.new_block(nonce=100,previous_hash=1)
        self.last_block = {} 
        self.minermoney = 100

    def _call_end(self): print(self.chain[-1]['index']) ; return self.chain[-1] if len(self.chain) else {}
    last_block = property(_call_end,lambda a,x:x) 

    def new_block(self,nonce,previous_hash=None):
        self.chain.append(block := {'index':len(self.chain)+1,
                                    'timestamp':time.time(),
                                    'transactions':self.cur_transactions,
                                    'nonce':nonce,
                                    'previous_hash':previous_hash or self.hash(self.chain[-1])})
        self.cur_transactions = []
        return block
    
    def new_transaction(self,sender,recipient,amount,sbal,rbal):
        
        self.current_transactions.append(trx :={
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        'sender-amt':sbal-amount,
        'recipient-amt':rbal+amount

        }) if sbal>=amount else 0
        return trx
    
    def proof_of_work(self,last_proof):
        proof=0
        while self.valid_proof(last_proof,proof) is False:
            proof+=1
        return proof  
    
    @staticmethod
    def valid_proof(last_proof,proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','')
blockchain = Blockchain()

@app.route('/mine',methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_nonce = last_block['nonce']
    nonce = blockchain.proof_of_work(last_nonce)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        sbal=1,
        rbal=blockchain.minermoney
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    