import os
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI")

_client = None

def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is required")
        _client = MongoClient(MONGODB_URI)
    return _client

def get_database():
    client = get_mongo_client()
    # Extract database name from URI, default to 'scout'
    return client.get_default_database(default='scout')
