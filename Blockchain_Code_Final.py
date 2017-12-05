import hashlib
import random
import json

def make_random_transaction():
    amount = random.randint(1, 5)
    alice = random.choice([-amount, amount])
    bob = -alice
    return {'Alice':alice, 'Bob':bob}

[make_random_transaction() for _ in range(10)]

def update_state(transaction, state):
    state = state.copy()
    for key in transaction:
        state[key] = state.get(key, 0) + transaction[key]
    return state

state = {'Alice':5, 'Bob':5}
transaction = {'Alice': -3, 'Bob': 3}
state = update_state(transaction, state)
state

def validate_transaction(transaction, state):
    if sum(transaction.values()):
        return False
    
    for key in transaction.keys():
        if state.get(key, 0) + transaction[key] < 0:
            return False

    return True

state = {'Alice':5, 'Bob':5}

assert validate_transaction({'Alice': -3, 'Bob': 3}, state)
assert not validate_transaction({'Alice': -4, 'Bob': 3}, state)
assert not validate_transaction({'Alice': -6, 'Bob': 6}, state)
assert validate_transaction({'Alice': -4, 'Bob': 2, 'Lisa': 2}, state)
assert not validate_transaction({'Alice': -4, 'Bob': 3, 'Lisa': 2}, state)

def hash_function(msg=''):
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)
    msg = str(msg).encode('utf-8')
    return hashlib.sha256(msg).hexdigest()

hash_function({'foo':'bar'})

state = {'Alice': 50, 'Bob': 50}
blockchain = []

block0_contents = {
    'number': 0,
    'parent_hash': None,
    'transactions_count': 1,
    'transactions': [state]
}

block0 = {
    'hash': hash_function(block0_contents),
    'contents': block0_contents
}

blockchain.append(block0)
blockchain

def make_block(transactions, chain):
    parent = chain[-1]

    contents = {
        'number': parent['contents']['number'] + 1,
        'parent_hash': parent['hash'],
        'transactions_count': len(transactions),
        'transactions': transactions
    }
    return {
        'hash': hash_function(contents),
        'contents': contents
    }
	

transactions = [make_random_transaction() for _ in range(15)]
transactions

block_size = 5

transactions_buffer = []
for transaction in transactions:
    if not validate_transaction(transaction, state):
        continue
        
    state = update_state(transaction, state)
    transactions_buffer.append(transaction)
    
    if len(transactions_buffer) == block_size:
        block = make_block(transactions_buffer, blockchain)
        blockchain.append(block)
        transactions_buffer = []
state

blockchain

def validate_block(block, parent, state):    
    error_msg = 'Error in %d' % block['contents']['number']

    # check block hash
    assert block['hash'] == hash_function(block['contents']), error_msg

    # check block numbers
    assert block['contents']['number'] == parent['contents']['number'] + 1, error_msg

    # check parent hash
    assert block['contents']['parent_hash'] == parent['hash'], error_msg
    
    # check transaction count
    assert len(block['contents']['transactions']) == block['contents']['transactions_count']
    
    # validate all transactions
    for transaction in block['contents']['transactions']:
        assert validate_transaction(transaction, state), error_msg
        state = update_state(transaction, state)
        
    return state
	
def check_chain(blockchain):
    state = {}

    for transaction in blockchain[0]['contents']['transactions']:
        state = update_state(transaction, state)

    parent = blockchain[0]
    
    for block in blockchain[1:]:
        state = validate_block(block, parent, state)
        parent = block

    return state

check_chain(blockchain)


