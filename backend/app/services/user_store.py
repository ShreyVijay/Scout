import os
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def ensure_preferences_index():
    try:
        if not es.indices.exists(index="user_preferences"):
            es.indices.create(
                index="user_preferences",
                mappings={
                    "properties": {
                        "email": {"type": "keyword"},
                        "preferences": {
                            "properties": {
                                "atmosphere_weight": {"type": "float"},
                                "budget_weight": {"type": "float"},
                                "transport_weight": {"type": "float"}
                            }
                        }
                    }
                }
            )
    except Exception:
        pass

def get_user(email: str) -> dict:
    from app.db.mongodb import get_database
    from app.db.collections import USERS_COLLECTION
    db = get_database()
    
    # Fetch identity from MongoDB
    user_doc = db[USERS_COLLECTION].find_one({"email": email}, {"_id": 0})
    if not user_doc:
        return None
        
    user = dict(user_doc)
    user["user_id"] = email  # Keep user_id for legacy compatibility
    
    # Fetch preferences from Elasticsearch
    ensure_preferences_index()
    try:
        res = es.get(index="user_preferences", id=email)
        user["preferences"] = res["_source"].get("preferences", {})
    except Exception:
        user["preferences"] = {
            "atmosphere_weight": 0.5,
            "budget_weight": 0.3,
            "transport_weight": 0.2
        }
        
    # User mission state
    user["current_mission"] = user_doc.get("current_mission")
    user["mission_history"] = user_doc.get("mission_history", [])
    
    return user

def save_user(user: dict) -> dict:
    from app.db.mongodb import get_database
    from app.db.collections import USERS_COLLECTION
    db = get_database()
    
    email = user["email"]
    name = user.get("name", "User")
    
    update_data = {
        "email": email, 
        "name": name,
        "current_mission": user.get("current_mission"),
        "mission_history": user.get("mission_history", [])
    }
    
    # Save identity to MongoDB
    db[USERS_COLLECTION].update_one(
        {"email": email},
        {"$set": update_data},
        upsert=True
    )
    
    # Save preferences to Elasticsearch
    if "preferences" in user:
        ensure_preferences_index()
        es.index(
            index="user_preferences",
            id=email,
            document={"email": email, "preferences": user["preferences"]}
        )
        
    return user
