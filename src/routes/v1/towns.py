from fastapi import APIRouter, HTTPException
from src.services.db import get_database
from src.config import MONGO_COLLECTION_NAME

router = APIRouter()

@router.get("/toptowns")
def toptowns():
    """
    Return top 25 towns by document count from MongoDB collection `towns`.
    Response JSON: {"Town": [...town names...], "Count": [...counts...] }
    """
    try:
        db = get_database() 
        #print("Using database:", db.name)
        #print("Collections:", db.list_collection_names())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"DB configuration error: {exc}")

    towns = db.get_collection(MONGO_COLLECTION_NAME)

    pipeline = [
        {
            "$group": {
                "_id": "$Town",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 25}
    ]

    try:
        cursor = towns.aggregate(pipeline)
        results = list(cursor)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query error: {e}")

    return results

@router.get("/townslist")
def townslist():
    """
    Return list of distinct towns from MongoDB collection `towns`.
    Response JSON: {"Towns": [...town names...] }
    """
    try:
        db = get_database() 
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"DB configuration error: {exc}")

    towns = db.get_collection(MONGO_COLLECTION_NAME)

    try:
        distinct_towns = towns.distinct("Town")
        distinct_towns.sort()  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query error: {e}")

    return {"Towns": distinct_towns}