from app.services.budget_profile_service import (
    create_budget_profile,
    get_budget_profile,
    update_budget_profile,
    delete_budget_profile
)
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()
es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def test_crud():
    print("--- Testing Budget Profile Service CRUD ---")

    # Clean profile before test
    test_id = "test-mission-999"
    delete_budget_profile(test_id)
    es.indices.refresh(index="budget_profiles")

    # 1. Create
    print("Testing create...")
    profile = {
        "profile_id": test_id,
        "mission_id": test_id,
        "team": "Egypt",
        "total_budget": 2500,
        "spent_budget": 100,
        "remaining_budget": 2400,
        "risk_level": "LOW"
    }
    create_budget_profile(profile)
    es.indices.refresh(index="budget_profiles")

    # 2. Read
    print("Testing read...")
    loaded = get_budget_profile(test_id)
    assert loaded is not None
    assert loaded["total_budget"] == 2500
    assert loaded["risk_level"] == "LOW"
    print("Read passed.")

    # 3. Update
    print("Testing update...")
    loaded["spent_budget"] = 600
    loaded["remaining_budget"] = 1900
    loaded["risk_level"] = "MEDIUM"
    update_budget_profile(loaded)
    es.indices.refresh(index="budget_profiles")
    
    updated = get_budget_profile(test_id)
    assert updated["spent_budget"] == 600
    assert updated["risk_level"] == "MEDIUM"
    print("Update passed.")

    # 4. Delete
    print("Testing delete...")
    delete_budget_profile(test_id)
    es.indices.refresh(index="budget_profiles")
    
    deleted = get_budget_profile(test_id)
    assert deleted is None
    print("Delete passed.")

    print("Budget Profile CRUD Tests Passed Successfully!\n")

if __name__ == "__main__":
    test_crud()
