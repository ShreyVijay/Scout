# backend/app/services/mission_preference_service.py

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime
from app.services.default_preferences import get_default_preferences
from app.services.fan_preference_service import get_preferences_by_mission

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def resolve_mission_preferences(mission_id):
    """
    Resolves preferences for a mission. 
    Lookups mission, checks for custom fan preferences, and falls back to defaults.
    """
    # 1. Lookup mission by mission_id
    result = es.search(
        index="missions",
        size=1,
        query={
            "term": {
                "mission_id": mission_id
            }
        }
    )
    hits = result["hits"]["hits"]
    if not hits:
        raise ValueError(f"Mission not found: {mission_id}")

    mission = hits[0]["_source"]

    # 2. Lookup preferences
    pref = get_preferences_by_mission(mission_id)
    if not pref:
        # 3. If missing, load default preferences fallback
        defaults = get_default_preferences()
        pref = {
            "preference_id": mission_id,
            "mission_id": mission_id,
            "team": mission.get("team"),
            "travel_style": mission.get("travel_style"),
            "atmosphere_weight": defaults["atmosphere_weight"],
            "budget_weight": defaults["budget_weight"],
            "transport_weight": defaults["transport_weight"],
            "preference_version": defaults["preference_version"],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

    return pref
