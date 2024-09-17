from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
import hashlib
import datetime  # Importando datetime

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Cria o bloco gênese
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, seller_name, seller_id, buyer_name, buyer_id, amount):
        self.current_transactions.append({
            'seller_name': seller_name,
            'seller_id': seller_id,
            'buyer_name': buyer_name,
            'buyer_id': buyer_id,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

app = Flask(__name__)
api = Api(app)
blockchain = Blockchain()

class Transaction(Resource):
    def post(self):
        data = request.get_json()
        if not all(key in data for key in ['seller_name', 'seller_id', 'buyer_name', 'buyer_id', 'amount']):
            return 'Missing values', 400

        seller_name = data['seller_name']
        seller_id = data['seller_id']
        buyer_name = data['buyer_name']
        buyer_id = data['buyer_id']
        amount = data['amount']

        if amount <= 0 or amount > 100:
            return 'Invalid amount', 400

        index = blockchain.new_transaction(seller_name, seller_id, buyer_name, buyer_id, amount)
        blockchain.new_block(proof=100)  # Aqui você pode usar um algoritmo de prova real
        return jsonify({
            'message': f'Transaction will be added to Block {index}'
        })

class BlockchainChain(Resource):
    def get(self):
        return jsonify({
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        })

api.add_resource(Transaction, '/transaction')
api.add_resource(BlockchainChain, '/chain')

if __name__ == '__main__':
    app.run(port=5000)
