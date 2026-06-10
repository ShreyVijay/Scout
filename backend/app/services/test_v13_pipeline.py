import os
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.services.mission_service import create_mission
from app.services.mission_store import get_latest_mission
from app.services.mission_city_service import get_mission_cities_intelligence

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def run_v13_pipeline():
    print("--- STARTING V1.3 CITY INTELLIGENCE PIPELINE TEST ---")

    # 1. Ensure test mission index exists and recreate a clean mission
    print("\nStep 1: Recreating missions index for clean pipeline test")
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

    # 2. Create Mission
    print("\nStep 2: Creating a mission for Egypt (itinerary includes New York, Dallas, Los Angeles)")
    mission = create_mission(
        team="Egypt",
        budget=4000,
        travel_style="Comfort",
        objective="Follow Egypt matches"
    )
    es.indices.refresh(index="missions")
    print(f"Mission created. Mission ID: {mission['mission_id']}, Team: {mission['team']}")
    
    # 3. Retrieve Mission
    print("\nStep 3: Retrieving latest mission from database")
    retrieved_mission = get_latest_mission("Egypt")
    assert retrieved_mission is not None
    assert retrieved_mission["mission_id"] == mission["mission_id"]
    print(f"Successfully retrieved mission from ES index: {retrieved_mission['mission_id']}")

    # 4. Resolve and Load Location/City/Stadium Intelligence for Itinerary
    print("\nStep 4: Resolving location intelligence for all itinerary cities")
    result = get_mission_cities_intelligence(retrieved_mission)
    
    # Assertions
    assert result["mission_id"] == retrieved_mission["mission_id"]
    print(f"Mission ID match: {result['mission_id']}")
    
    # Verify unique cities (New York, Dallas, Los Angeles)
    cities_payload = result["cities"]
    print(f"Total unique cities resolved: {len(cities_payload)}")
    assert len(cities_payload) == 3, f"Expected 3 unique cities, got {len(cities_payload)}"
    
    resolved_names = [c["city"] for c in cities_payload]
    print(f"Resolved city names: {resolved_names}")
    assert "New York" in resolved_names
    assert "Dallas" in resolved_names
    assert "Los Angeles" in resolved_names

    # Verify stadium nesting and scores for each resolved city
    for city_intel in cities_payload:
        city_name = city_intel["city"]
        print(f"\nVerifying city: {city_name}")
        assert city_intel["country"] == "USA"
        assert city_intel["atmosphere_score"] > 0
        assert city_intel["budget_score"] > 0
        assert city_intel["transport_score"] > 0
        assert city_intel["fan_zone_score"] > 0
        assert city_intel["description"] != ""
        
        # Verify stadiums mapping
        stadiums = city_intel["stadiums"]
        print(f"  Associated stadiums count: {len(stadiums)}")
        assert len(stadiums) > 0, f"City {city_name} should have at least 1 stadium"
        
        for stadium in stadiums:
            print(f"    - Stadium Name: {stadium['stadium']}")
            assert stadium["city"] == city_name
            assert stadium["capacity"] > 0
            assert stadium["atmosphere_score"] > 0
            assert stadium["transport_score"] > 0
            assert stadium["description"] != ""

    print("\n--- V1.3 PIPELINE VERIFICATION PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_v13_pipeline()
