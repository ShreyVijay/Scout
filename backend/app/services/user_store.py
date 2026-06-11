import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def ensure_users_index():
    try:
        if not es.indices.exists(index="users"):
            es.indices.create(
                index="users",
                mappings={
                    "properties": {
                        "user_id": {"type": "keyword"},
                        "email": {"type": "keyword"},
                        "name": {"type": "text"},
                        "preferences": {
                            "properties": {
                                "atmosphere_weight": {"type": "float"},
                                "budget_weight": {"type": "float"},
                                "transport_weight": {"type": "float"}
                            }
                        },
                        "saved_missions": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"}
                    }
                }
            )
    except Exception:
        pass  # Gracefully ignore if index already exists or creation fails due to network

def get_user(user_id: str) -> dict:
    ensure_users_index()
    try:
        res = es.get(index="users", id=user_id)
        user = res["_source"]
        return user
    except Exception:
        if user_id == "default-fan":
            # Initialize default user
            default_user = {
                "user_id": "default-fan",
                "email": "fan@fifa2026.com",
                "name": "Super Fan",
                "preferences": {
                    "atmosphere_weight": 0.5,
                    "budget_weight": 0.3,
                    "transport_weight": 0.2
                },
                "saved_missions": [],
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            save_user(default_user)
            return default_user
        return None

def save_user(user: dict) -> dict:
    ensure_users_index()
    user["updated_at"] = datetime.utcnow().isoformat()
    if "created_at" not in user or not user["created_at"]:
        user["created_at"] = datetime.utcnow().isoformat()
    
    # Exclude metadata from doc body
    doc = {k: v for k, v in user.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}
    
    es.index(
        index="users",
        id=user["user_id"],
        document=doc
    )
    return user
