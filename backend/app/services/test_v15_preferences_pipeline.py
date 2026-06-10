# backend/app/services/test_v15_preferences_pipeline.py

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.services.mission_service import create_mission
from app.services.mission_store import get_latest_mission
from app.services.mission_preference_service import resolve_mission_preferences
from app.services.fan_preference_service import create_preferences, get_preferences_by_mission
from app.services.create_fan_preferences_index import create_index as create_pref_index

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def run_pipeline_test():
    print("--- STARTING V1.5 PREFERENCES PIPELINE INTEGRATION TEST ---")

    # 1. Clean indices
    print("\nStep 1: Recreating missions index and fan_preferences index")
    create_pref_index()
    if es.indices.exists(index="missions"):
        es.indices.delete(index="missions")
    es.indices.create(
        index="missions",
        mappings={
            "properties": {
                "mission_id": {"type": "keyword"},
                "team": {"type": "keyword"},
                "budget": {
                    "properties": {
                        "total_budget": {"type": "integer"},
                        "spent_budget": {"type": "integer"},
                        "estimated_cost": {"type": "integer"},
                        "remaining_budget": {"type": "integer"},
                        "risk_level": {"type": "keyword"}
                    }
                },
                "travel_style": {"type": "keyword"},
                "objective": {"type": "text"},
                "mission_state": {"type": "keyword"},
                "tournament_state": {"type": "keyword"},
                "requires_replanning": {"type": "boolean"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
                "itinerary": {
                    "type": "nested",
                    "properties": {
                        "city": {"type": "keyword"},
                        "stadium": {"type": "text"},
                        "date": {"type": "date"}
                    }
                },
                "state_history": {
                    "type": "nested",
                    "properties": {
                        "state_type": {"type": "keyword"},
                        "from": {"type": "keyword"},
                        "to": {"type": "keyword"},
                        "timestamp": {"type": "date"}
                    }
                }
            }
        }
    )
    es.indices.refresh(index="missions")
    es.indices.refresh(index="fan_preferences")

    # 2. Create Mission
    print("\nStep 2: Creating planned mission for Egypt")
    mission = create_mission(
        team="Egypt",
        budget=3500,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    
    mission_id = mission["mission_id"]
    print(f"Created Mission ID: {mission_id}, Travel Style: {mission['travel_style']}")

    # 3. Test Preference Lookup with Default Fallback
    print("\nStep 3: Resolving preferences (expecting default fallback)")
    resolved_default = resolve_mission_preferences(mission_id)
    print(f"Resolved default fallback preferences: {resolved_default}")

    assert resolved_default["preference_id"] == mission_id
    assert resolved_default["mission_id"] == mission_id
    assert resolved_default["team"] == "Egypt"
    assert resolved_default["travel_style"] == "Comfort"
    assert resolved_default["atmosphere_weight"] == 0.5
    assert resolved_default["budget_weight"] == 0.3
    assert resolved_default["transport_weight"] == 0.2
    assert resolved_default["preference_version"] == 1

    # 4. Store Custom Preferences
    print("\nStep 4: Storing custom weights (0.1, 0.8, 0.1)")
    custom_pref = {
        "preference_id": mission_id,
        "mission_id": mission_id,
        "team": "Egypt",
        "travel_style": "Comfort",
        "atmosphere_weight": 0.1,
        "budget_weight": 0.8,
        "transport_weight": 0.1
    }
    create_preferences(custom_pref)
    es.indices.refresh(index="fan_preferences")

    # 5. Resolve Again (should now return custom weights)
    print("\nStep 5: Resolving preferences (expecting custom weights lookup)")
    resolved_custom = resolve_mission_preferences(mission_id)
    print(f"Resolved custom stored preferences: {resolved_custom}")

    assert resolved_custom["atmosphere_weight"] == 0.1
    assert resolved_custom["budget_weight"] == 0.8
    assert abs(resolved_custom["transport_weight"] - 0.1) < 1e-9

    print("\n--- V1.5 PREFERENCES PIPELINE INTEGRATION TEST PASSED SUCCESSFULLY ---")

if __name__ == "__main__":
    run_pipeline_test()
