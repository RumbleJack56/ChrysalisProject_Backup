import hashlib
import time
import json
from uuid import uuid4
from flask import Flask,jsonify,request


class Blockchain(object):
    def __init__(self):
        #defines blockchain, transaction pool, genesis block
        self.chain = []
        self.cur_transactions = []
        self.new_block(proof=100,previous_hash=1)
    
    #makes new block of blockchain returns the block
    def new_block(self,proof,previous_hash=None):  
        self.chain.append(block := {'index': len(self.chain)+1,
                           'timestamp': time.time(),
                           'transactions': self.cur_transactions,
                           'proof': proof,
                           'previous_hash': previous_hash or self.hash(self.chain[-1])
                           })
        self.cur_transactions = []
        return block
    
    def new_transaction(self,sender,recipient,amount):
        self.current_transactions.append({
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        })

        return self.last_block['index'] + 1


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
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
     # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def api_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)