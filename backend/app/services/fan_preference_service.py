# backend/app/services/fan_preference_service.py

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime
from app.services.preference_validator import normalize_weights

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def create_preferences(preferences):
    """
    Saves a new fan preference document using preference_id as document ID.
    Enforces normalization of weight values and adds creation metadata.
    """
    preferences["created_at"] = datetime.utcnow().isoformat()
    preferences["updated_at"] = datetime.utcnow().isoformat()
    
    # Enforce default version if not present
    if "preference_version" not in preferences:
        preferences["preference_version"] = 1

    # Normalize weights before saving
    norm_atm, norm_bud, norm_tr = normalize_weights(
        preferences.get("atmosphere_weight", 0.0),
        preferences.get("budget_weight", 0.0),
        preferences.get("transport_weight", 0.0)
    )
    preferences["atmosphere_weight"] = norm_atm
    preferences["budget_weight"] = norm_bud
    preferences["transport_weight"] = norm_tr

    doc = {k: v for k, v in preferences.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}
    pref_id = preferences["preference_id"]

    response = es.index(
        index="fan_preferences",
        id=pref_id,
        document=doc
    )

    preferences["_elastic_id"] = response["_id"]
    preferences["_seq_no"] = response["_seq_no"]
    preferences["_primary_term"] = response["_primary_term"]

    return preferences

def get_preferences(preference_id):
    """
    Fetches a fan preference document by document ID.
    Includes optimistic locking metadata.
    """
    try:
        result = es.get(
            index="fan_preferences",
            id=preference_id
        )
        pref = result["_source"]
        pref["_elastic_id"] = result["_id"]
        pref["_seq_no"] = result["_seq_no"]
        pref["_primary_term"] = result["_primary_term"]
        return pref
    except Exception:
        return None

def get_preferences_by_mission(mission_id):
    """
    Queries Elasticsearch to find a preference document associated with mission_id.
    """
    try:
        result = es.search(
            index="fan_preferences",
            size=1,
            seq_no_primary_term=True,
            query={
                "term": {
                    "mission_id": mission_id
                }
            }
        )
        hits = result["hits"]["hits"]
        if not hits:
            return None
        pref = hits[0]["_source"]
        pref["_elastic_id"] = hits[0]["_id"]
        pref["_seq_no"] = hits[0]["_seq_no"]
        pref["_primary_term"] = hits[0]["_primary_term"]
        return pref
    except Exception:
        return None

def update_preferences(preferences):
    """
    Updates an existing preference document with optimistic locking verification.
    Weights are automatically re-normalized on update.
    """
    preferences["updated_at"] = datetime.utcnow().isoformat()
    pref_id = preferences.get("preference_id")
    seq_no = preferences.get("_seq_no")
    primary_term = preferences.get("_primary_term")

    # Enforce default version if not present
    if "preference_version" not in preferences:
        preferences["preference_version"] = 1

    # Normalize weights before saving
    norm_atm, norm_bud, norm_tr = normalize_weights(
        preferences.get("atmosphere_weight", 0.0),
        preferences.get("budget_weight", 0.0),
        preferences.get("transport_weight", 0.0)
    )
    preferences["atmosphere_weight"] = norm_atm
    preferences["budget_weight"] = norm_bud
    preferences["transport_weight"] = norm_tr

    doc = {k: v for k, v in preferences.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}

    update_params = {
        "index": "fan_preferences",
        "id": pref_id,
        "doc": doc
    }

    if seq_no is not None and primary_term is not None:
        update_params["if_seq_no"] = seq_no
        update_params["if_primary_term"] = primary_term

    response = es.update(**update_params)

    if "result" in response and response["result"] in ["updated", "noop"]:
        if "_seq_no" in response:
            preferences["_seq_no"] = response["_seq_no"]
        if "_primary_term" in response:
            preferences["_primary_term"] = response["_primary_term"]

    return preferences

def delete_preferences(preference_id):
    """
    Deletes the preference document by ID.
    """
    try:
        response = es.delete(
            index="fan_preferences",
            id=preference_id
        )
        return response
    except Exception as e:
        return None
