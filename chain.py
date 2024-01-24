import hashlib
import time
import json



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

    @property
    def last_block(self):
        return self.chain[-1]
    

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