from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os, urllib.parse

load_dotenv()

DB_COLLECTION_NAME = os.getenv('DB_COLLECTION_NAME')

# Account on the cloud
mongo_client = MongoClient(f"mongodb+srv://{urllib.parse.quote_plus(os.getenv('MONGODB_USERNAME'))}:{urllib.parse.quote_plus(os.getenv('MONGODB_PASSWORD'))}@{os.getenv('DB_CLUSTER')}.{os.getenv('DB_NAME')}.mongodb.net/?retryWrites=true&w=majority")
db_client = mongo_client.production

def insert_RCA_collection(data):
    # Check if an entry with the same 'contract' value already exists
    existing_entry = db_client.DB_COLLECTION_NAME.find_one({'contract': data['contract_address']})

    if existing_entry:
        print(f"Entry with contract {data['contract_address']} already exists with ObjectID: {existing_entry['_id']}")
    else:
        # If not, insert the new data
        result = db_client.DB_COLLECTION_NAME.insert_one(data)
        print(f"Inserted data with ObjectID: {result.inserted_id}")

def check_RCA_in_db(contract_address):
    result = db_client.DB_COLLECTION_NAME.find_one({'contract':contract_address})
    print(result)