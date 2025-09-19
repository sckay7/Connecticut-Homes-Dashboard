from typing import Optional
from src.config import MONGODB_URI, MONGODB_DB

try:
    from pymongo import MongoClient
except Exception as e:
    raise RuntimeError("pymongo is required. Install with: pip install pymongo") from e


def get_mongo_client(uri: Optional[str] = None) -> MongoClient:
    """Return a MongoClient using MONGODB_URI or the provided uri."""
    uri = uri or MONGODB_URI or "mongodb://localhost:27017"
    return MongoClient(uri)


def get_database(db_name: Optional[str] = None, client: Optional[MongoClient] = None):
    """Return a Database instance.

    Priority: explicit db_name arg -> MONGODB_DB env -> default DB from URI -> error
    """
    if client is None:
        client = get_mongo_client()

    if db_name:
        return client[db_name]

    if MONGODB_DB:
        return client[MONGODB_DB]

    default = client.get_default_database()
    if default is not None:
        return default

    raise RuntimeError(
        "No database specified. Provide db_name, set MONGODB_DB env var, or include DB in the URI."
    )


__all__ = ["get_mongo_client", "get_database"]
