import os
import pymongo
from dotenv import load_dotenv

load_dotenv()  
MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", None)

def get_database(
    db_name: str = MONGO_DB_NAME, client: pymongo.MongoClient = None
) -> pymongo.database.Database:
    """
    Return a Database instance.
    """
    if client is None:
        if not MONGODB_URI:
            raise RuntimeError("MONGODB_URI is not set in environment")
        client = pymongo.MongoClient(MONGODB_URI)

    if db_name:
        return client[db_name]

    if client is not None and client.get_default_database() is not None:
        return client.get_default_database()

    raise RuntimeError("No database name provided and no default DB in URI")
