import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.services.mission_service import create_mission
from app.services.mission_store import get_latest_mission
from app.services.replanning_engine import run_replanning
from app.services.replanning_candidate_service import get_candidates

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def run_v15_pipeline():
    print("--- STARTING V1.5 ADAPTIVE REPLANNING PIPELINE TEST ---")

    # 1. Clean indices
    print("\nStep 1: Recreating missions index")
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
    print("\nStep 2: Creating planned mission for Egypt")
    mission = create_mission(
        team="Egypt",
        budget=3000,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    print(f"Created Mission ID: {mission['mission_id']}, Initial State: {mission['mission_state']}")

    # 3. Retrieve Mission
    mission = get_latest_mission("Egypt")

    # 4. Generate Candidates Directly to Verify Count > 0
    print("\nStep 3: Verifying candidate generation")
    candidates = get_candidates(mission)
    print(f"Candidates list: {candidates}")
    assert len(candidates) > 0, f"Expected candidate count > 0, got {len(candidates)}"

    # 5. Trigger Replanning Pipeline
    print("\nStep 4: Triggering replanning engine pipeline")
    result = run_replanning(mission)
    print(f"Replanning Result: {result}")

    # 6. Verify Pipeline Assertions
    print("\nStep 5: Verifying recommendation and reasoning outputs")
    
    assert result is not None
    assert "recommendation" in result
    assert "reasoning" in result

    rec = result["recommendation"]
    reasoning = result["reasoning"]

    audit = result["audit"]

    assert "audit" in result

    assert audit["winner"] == rec["city"]

    assert len(
        audit["audit"]
    ) == len(
        result["rankings"]
    )

    # Verify recommendation fields
    assert rec is not None
    assert "city" in rec
    assert rec["city"] is not None and rec["city"] != ""
    assert "match" in rec
    assert "reason" in rec

    # Verify reasoning fields

    assert reasoning is not None

    assert "decision" in reasoning

    assert "top_factors" in reasoning

    assert "contributions" in reasoning

    assert "final_score" in reasoning

    assert reasoning["decision"] == rec["city"]

    assert len(
        reasoning["top_factors"]
    ) > 0

    assert len(
        reasoning["contributions"]
    ) > 0

    assert rec["rank"] == 1

    if len(result["rankings"]) > 1:

        assert (
            rec["final_score"]
            >=
            result["rankings"][1]["final_score"]
        )

    print("\n--- V1.5 REPLANNING PIPELINE VERIFICATION PASSED SUCCESSFULLY ---")

if __name__ == "__main__":
    run_v15_pipeline()