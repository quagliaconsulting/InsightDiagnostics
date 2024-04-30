from pymongo import MongoClient
import os

mongo_db = None

def get_mongo_db():
    global mongo_db
    if mongo_db is None:
        connStr = os.getenv('MONGO_CONNECTION_URL')
        client = MongoClient(connStr, uuidRepresentation='standard')
        mongo_db = client['patientsort']
    return mongo_db