import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.mcp.tools.recommendation_tools import get_replanning_recommendation
from app.services.mission_service import create_mission

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)


def run_tests():
    print("--- STARTING MCP RECOMMENDATION TOOL TESTS ---")

    # 1. Clean / create test environment
    print("\nEnsuring mission exists for 'Egypt'...")
    mission = create_mission(
        team="Egypt",
        budget=3000,
        travel_style="Comfort",
        objective="Support Egypt"
    )
    es.indices.refresh(index="missions")
    print(f"Created/verified mission for Egypt. Mission ID: {mission['mission_id']}")

    # 2. Test get_replanning_recommendation
    print("\nTesting get_replanning_recommendation for 'Egypt'...")
    res = get_replanning_recommendation(team="Egypt")
    print(f"Replanning recommendation result: {res}")

    assert res["success"] is True
    data = res["data"]
    assert data is not None
    assert "recommendation" in data
    assert "reasoning" in data
    assert "rankings" in data

    rec = data["recommendation"]
    assert "city" in rec
    assert rec["city"] is not None and rec["city"] != ""
    assert "match" in rec
    assert "reason" in rec
    assert "rank" in rec

    reasoning = data["reasoning"]
    assert reasoning["decision"] == rec["city"]
    assert "top_factors" in reasoning
    assert "contributions" in reasoning
    assert "final_score" in reasoning

    print("Replanning recommendation tool test passed!")
    print("--- ALL MCP RECOMMENDATION TOOL TESTS PASSED ---")


if __name__ == "__main__":
    run_tests()
