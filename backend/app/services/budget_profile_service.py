import os
from datetime import datetime
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def create_budget_profile(profile):
    """Index a budget profile into Elasticsearch. Use profile_id as the document ID."""
    profile["created_at"] = datetime.utcnow().isoformat()
    profile["updated_at"] = datetime.utcnow().isoformat()
    
    doc_id = profile["profile_id"]
    response = es.index(
        index="budget_profiles",
        id=doc_id,
        document=profile
    )
    return response

def get_budget_profile(profile_id):
    """Retrieve budget profile by ID."""
    try:
        response = es.get(
            index="budget_profiles",
            id=profile_id
        )
        return response["_source"]
    except Exception:
        return None

def update_budget_profile(profile):
    """Update existing budget profile."""
    profile["updated_at"] = datetime.utcnow().isoformat()
    
    doc_id = profile["profile_id"]
    response = es.index(
        index="budget_profiles",
        id=doc_id,
        document=profile
    )
    return response

def delete_budget_profile(profile_id):
    """Delete budget profile by ID."""
    try:
        response = es.delete(
            index="budget_profiles",
            id=profile_id
        )
        return response
    except Exception:
        return None
