from web3 import Web3, exceptions
import os, requests
from dotenv import load_dotenv

load_dotenv()

POLYGON_MAINNET_API = os.getenv('POLYGON_MAINNET_API')
REDDIT_CONTRACT_ADDRESS = os.getenv('REDDIT_CONTRACT_ADDRESS')
POLYGONSCAN_API_KEY = os.getenv('POLYGONSCAN_API_KEY')

# start of the web3 related functions that scan the blockchain
if not POLYGON_MAINNET_API:
    print("API key not set")
else:
    w3 = Web3(Web3.HTTPProvider(POLYGON_MAINNET_API))

    if not w3.is_connected():
        print("Not connected to the Polygon network")
    else:
        def was_contract_created_by_reddit(contract_address, transaction_hash=None):
            contract_address = Web3.to_checksum_address(contract_address)

            # Check if contract code exists at the given address
            contract_code = w3.eth.get_code(contract_address)
            if contract_code == b'':
                print(f"No contract code found at address {contract_address}")
                return False
            
            try:
                # Get the transaction hash of the contract creation
                contract_creation_tx_hash = w3.eth.get_transaction_receipt(transaction_hash).transactionHash

                # Retrieve the transaction details
                transaction = w3.eth.get_transaction(contract_creation_tx_hash)

                # Check if the 'from' address of the transaction matches the specified creator address
                return transaction['from'].lower() == REDDIT_CONTRACT_ADDRESS.lower()
            except exceptions.TransactionNotFound:
                print(f"Transaction not found for contract address {contract_address}. It might not have been mined yet.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False

        def get_contract_creation_tx_hash(contract_address):
            try:
                # Convert the contract address to its checksum format
                contract_address = Web3.to_checksum_address(contract_address)

                # Get the transaction hash of the contract creation
                contract_creation_tx_hash = w3.eth.get_transaction_receipt(contract_address).transaction_hash
                
                return contract_creation_tx_hash.hex()
            except exceptions.TransactionNotFound:
                print(f"Transaction not found for contract address {contract_address}. It might not have been mined yet.")
                return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        # finds out which address minted the contract
        def get_transaction_creator(transaction_hash):
            """
            Get the address that created the given transaction.

            Parameters:
            - w3: Web3 instance connected to the desired network.
            - transaction_hash: Hash of the transaction to inspect.

            Returns:
            - Address of the creator of the transaction.
            """

            # Fetch the transaction details
            try:
                transaction = w3.eth.get_transaction(transaction_hash)
                return transaction['from']
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

# Polygonscan related functions

# this function will check when the contract was minted and give the transaction hash
def get_contract_creation_tx_hash(contract_address):
    base_url = "https://api.polygonscan.com/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": contract_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": POLYGONSCAN_API_KEY
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Check for a valid response
    if data['status'] == '1' and len(data['result']) > 0:
        # Return the transaction hash of the first transaction (creation)
        return data['result'][0]['hash']
    else:
        print(f"Error or no transactions found for address {contract_address}. Message: {data['message']}")
        return None
    
def get_contract_creations(address):
    base_url = f"https://api.polygonscan.com/api"
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': POLYGONSCAN_API_KEY
    }
    
    response = requests.get(base_url, params=params)
    transactions = response.json().get('result', [])
    
    contract_creations = []
    for tx in transactions:
        # Check if the transaction has a contractAddress field (indicative of contract creation)
        if tx.get('contractAddress'):
            contract_creations.append({
                'contract_address': tx['contractAddress'],
                'transaction_hash': tx['hash']
            })
            
    return contract_creations