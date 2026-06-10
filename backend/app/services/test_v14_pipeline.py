import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.services.mission_service import create_mission
from app.services.mission_store import get_latest_mission, update_mission
from app.services.mission_budget_service import integrate_mission_budget
from app.services.budget_profile_service import create_budget_profile, get_budget_profile

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def run_v14_pipeline():
    print("--- STARTING V1.4 BUDGET ENGINE PIPELINE TEST ---")

    # 1. Clean indices
    print("\nStep 1: Recreating missions and budget_profiles indices")
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

    if es.indices.exists(index="budget_profiles"):
        es.indices.delete(index="budget_profiles")
    es.indices.create(
        index="budget_profiles",
        mappings={
            "properties": {
                "profile_id": {"type": "keyword"},
                "mission_id": {"type": "keyword"},
                "team": {"type": "keyword"},
                "total_budget": {"type": "integer"},
                "spent_budget": {"type": "integer"},
                "remaining_budget": {"type": "integer"},
                "risk_level": {"type": "keyword"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"}
            }
        }
    )
    es.indices.refresh(index="missions")
    es.indices.refresh(index="budget_profiles")

    # 2. Create Mission
    print("\nStep 2: Creating planned mission for Egypt with budget 2500")
    mission = create_mission(
        team="Egypt",
        budget=2500,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    print(f"Created Mission ID: {mission['mission_id']}, Initial State: {mission['mission_state']}")

    # 3. Integrate Budget & Perform Risk Calculations
    print("\nStep 3: Integrating budget intelligence")
    mission = get_latest_mission("Egypt")
    # Spent budget is initially 0
    mission = integrate_mission_budget(mission, spent_budget=0)
    update_mission(mission)
    es.indices.refresh(index="missions")
    
    # 4. Persist Budget Profile state
    print("\nStep 4: Persisting Budget Profile to Elasticsearch")
    intel = mission["budget"]
    profile = {
        "profile_id": mission["mission_id"],
        "mission_id": mission["mission_id"],
        "team": mission["team"],
        "total_budget": intel["total_budget"],
        "spent_budget": intel["spent_budget"],
        "remaining_budget": intel["remaining_budget"],
        "risk_level": intel["risk_level"]
    }
    create_budget_profile(profile)
    es.indices.refresh(index="budget_profiles")

    # 5. Reload and Assert Output
    print("\nStep 5: Verifying persisted states and assertions")
    retrieved_mission = get_latest_mission("Egypt")
    retrieved_profile = get_budget_profile(mission["mission_id"])

    print(f"Retrieved Mission Budget Object: {retrieved_mission['budget']}")
    print(f"Retrieved Budget Profile Document: {retrieved_profile}")

    # Assertions
    assert retrieved_mission["budget"] is not None
    assert retrieved_mission["budget"]["estimated_cost"] == 670, f"Expected 670, got {retrieved_mission['budget']['estimated_cost']}"
    assert retrieved_mission["budget"]["remaining_budget"] == 2500
    assert retrieved_mission["budget"]["risk_level"] == "LOW"

    assert retrieved_profile is not None
    assert retrieved_profile["total_budget"] == 2500
    assert retrieved_profile["spent_budget"] == 0
    assert retrieved_profile["remaining_budget"] == 2500
    assert retrieved_profile["risk_level"] == "LOW"

    print("\n--- V1.4 BUDGET ENGINE PIPELINE VERIFICATION PASSED SUCCESSFULLY ---")

if __name__ == "__main__":
    run_v14_pipeline()
