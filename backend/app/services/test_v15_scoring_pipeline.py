# backend/app/services/test_v15_scoring_pipeline.py
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.services.mission_service import create_mission
from app.services.mission_store import get_latest_mission
from app.services.fan_preference_service import create_preferences
from app.services.create_fan_preferences_index import create_index as create_pref_index
from app.services.replanning_engine import run_replanning
from app.services.load_cities import load_cities
from app.services.load_stadiums import load_stadiums
from app.services.load_alternatives import load_alternatives

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def setup_test_environment():
    print("Recreating indices for clean test environment...")
    
    # Recreate missions index
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

    create_pref_index()
    load_alternatives()
    load_cities()
    load_stadiums()
    
    es.indices.refresh(index="missions")
    es.indices.refresh(index="fan_preferences")
    es.indices.refresh(index="alternative_routes")
    es.indices.refresh(index="cities")
    es.indices.refresh(index="stadiums")

def run_pipeline_tests():
    print("--- STARTING V1.5 PIPELINE SCORING INTEGRATION TESTS ---")

    # ==========================================
    # Scenario 1: Atmosphere-heavy (Miami wins)
    # ==========================================
    print("\n=== Scenario 1: Atmosphere-heavy ===")
    setup_test_environment()
    
    mission = create_mission(
        team="Egypt",
        budget=3000,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    
    pref = {
        "preference_id": "pref-scen-1",
        "mission_id": mission["mission_id"],
        "team": "Egypt",
        "atmosphere_weight": 0.8,
        "budget_weight": 0.1,
        "transport_weight": 0.1
    }
    create_preferences(pref)
    es.indices.refresh(index="fan_preferences")
    
    mission = get_latest_mission("Egypt")
    result = run_replanning(mission)
    
    assert result["recommendation"] is not None
    assert result["recommendation"]["city"] == "Miami", f"Expected Miami to win Atmosphere-heavy scenario, got {result['recommendation']['city']}"
    assert result["rankings"][0]["city"] == "Miami"
    assert result["rankings"][1]["city"] == "Los Angeles"
    assert result["rankings"][2]["city"] == "Kansas City"
    
    assert result["rankings"][0]["final_score"] >= result["rankings"][1]["final_score"]
    assert result["rankings"][1]["final_score"] >= result["rankings"][2]["final_score"]
    
    assert result["reasoning"]["top_factors"] == ["atmosphere", "transport", "budget"]
    print("Scenario 1 passed!")

    # ==========================================
    # Scenario 2: Budget-heavy (Kansas City wins)
    # ==========================================
    print("\n=== Scenario 2: Budget-heavy ===")
    setup_test_environment()
    
    mission = create_mission(
        team="Egypt",
        budget=3000,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    
    pref = {
        "preference_id": "pref-scen-2",
        "mission_id": mission["mission_id"],
        "team": "Egypt",
        "atmosphere_weight": 0.1,
        "budget_weight": 0.8,
        "transport_weight": 0.1
    }
    create_preferences(pref)
    es.indices.refresh(index="fan_preferences")
    
    mission = get_latest_mission("Egypt")
    result = run_replanning(mission)
    
    assert result["recommendation"] is not None
    assert result["recommendation"]["city"] == "Kansas City", f"Expected Kansas City to win Budget-heavy scenario, got {result['recommendation']['city']}"
    assert result["rankings"][0]["city"] == "Kansas City"
    assert result["rankings"][0]["final_score"] >= result["rankings"][1]["final_score"]
    
    assert len(
        result["reasoning"]["top_factors"]
    ) == 3
    print("Scenario 2 passed!")

    # ==========================================
    # Scenario 3: Transport-heavy (Los Angeles wins)
    # ==========================================
    print("\n=== Scenario 3: Transport-heavy ===")
    setup_test_environment()
    
    mission = create_mission(
        team="Egypt",
        budget=3000,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    
    pref = {
        "preference_id": "pref-scen-3",
        "mission_id": mission["mission_id"],
        "team": "Egypt",
        "atmosphere_weight": 0.1,
        "budget_weight": 0.1,
        "transport_weight": 0.8
    }
    create_preferences(pref)
    es.indices.refresh(index="fan_preferences")
    
    mission = get_latest_mission("Egypt")
    result = run_replanning(mission)
    
    assert result["recommendation"] is not None
    assert result["recommendation"]["city"] == "Los Angeles", f"Expected Los Angeles to win Transport-heavy scenario, got {result['recommendation']['city']}"
    assert result["rankings"][0]["city"] == "Los Angeles"
    assert result["rankings"][0]["final_score"] >= result["rankings"][1]["final_score"]
    
    assert result["reasoning"]["top_factors"] == ["transport", "atmosphere", "budget"]
    print("Scenario 3 passed!")

    # ==========================================
    # Scenario 4: Low Budget Proportional Penalty (Kansas City wins)
    # ==========================================
    print("\n=== Scenario 4: Proportional Penalty ===")
    setup_test_environment()
    
    mission = create_mission(
        team="Egypt",
        budget=150,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    
    pref = {
        "preference_id": "pref-scen-4",
        "mission_id": mission["mission_id"],
        "team": "Egypt",
        "atmosphere_weight": 0.8,
        "budget_weight": 0.1,
        "transport_weight": 0.1
    }
    create_preferences(pref)
    es.indices.refresh(index="fan_preferences")
    
    mission = get_latest_mission("Egypt")
    # Manually inject budget intelligence for this penalty test to guarantee remaining budget is 150
    mission["budget_intelligence"] = {
        "total_budget": 150,
        "spent_budget": 0,
        "estimated_cost": 0,
        "projected_remaining_budget": 150,
        "risk_level": "LOW"
    }
    
    result = run_replanning(mission)
    
    assert result["recommendation"] is not None
    assert result["recommendation"]["city"] == "Kansas City", f"Expected Kansas City to win due to budget penalty, got {result['recommendation']['city']}"
    assert result["rankings"][0]["city"] == "Kansas City"
    
    print("Scenario 4 passed!")

    print("--- ALL V1.5 PIPELINE SCORING INTEGRATION TESTS PASSED SUCCESSFULLY ---")

if __name__ == "__main__":
    run_pipeline_tests()
