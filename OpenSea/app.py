from web3_utils import get_contract_creations
from db_commands import insert_RCA_collection
import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CONTRACT_ADDRESS = os.getenv('REDDIT_CONTRACT_ADDRESS')

created_contracts = get_contract_creations(REDDIT_CONTRACT_ADDRESS)

for contract in created_contracts:
    insert_RCA_collection(contract)
    print(f'successfully inserted {contract}')