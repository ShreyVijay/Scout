# backend/app/services/test_fan_preferences.py

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.services.fan_preference_service import (
    create_preferences,
    get_preferences,
    get_preferences_by_mission,
    update_preferences,
    delete_preferences
)
from app.services.create_fan_preferences_index import create_index

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def run_tests():
    print("--- STARTING FAN PREFERENCE SERVICE UNIT TESTS ---")

    # 1. Clean and recreate index
    print("\nStep 1: Recreating fan_preferences index")
    create_index()
    es.indices.refresh(index="fan_preferences")

    # 2. Test create_preferences and weights normalization
    print("\nStep 2: Creating preference with non-normalized weights (0.9, 0.9, 0.9)")
    pref = {
        "preference_id": "pref-test-1",
        "mission_id": "mission-test-1",
        "team": "Egypt",
        "travel_style": "Comfort",
        "atmosphere_weight": 0.9,
        "budget_weight": 0.9,
        "transport_weight": 0.9,
        "preference_version": 1
    }

    created = create_preferences(pref)
    es.indices.refresh(index="fan_preferences")

    print(f"Created preference document: {created}")
    
    # Assertions on normalization
    total_weights = created["atmosphere_weight"] + created["budget_weight"] + created["transport_weight"]
    assert abs(total_weights - 1.0) < 1e-9, f"Expected weights sum to be exactly 1.0, got {total_weights}"
    assert abs(created["atmosphere_weight"] - 0.3333333333333333) < 1e-9, f"Expected 0.3333, got {created['atmosphere_weight']}"
    assert abs(created["budget_weight"] - 0.3333333333333333) < 1e-9, f"Expected 0.3333, got {created['budget_weight']}"
    assert abs(created["transport_weight"] - 0.3333333333333334) < 1e-9, f"Expected 0.3334, got {created['transport_weight']}"

    # Verify optimistic concurrency metadata presence
    assert "_seq_no" in created
    assert "_primary_term" in created

    # 3. Test get_preferences and get_preferences_by_mission
    print("\nStep 3: Retrieving preference doc from Elasticsearch")
    retrieved_by_id = get_preferences("pref-test-1")
    retrieved_by_mission = get_preferences_by_mission("mission-test-1")

    assert retrieved_by_id is not None
    assert retrieved_by_mission is not None
    assert retrieved_by_id["preference_id"] == "pref-test-1"
    assert retrieved_by_mission["preference_id"] == "pref-test-1"
    print(f"Successfully retrieved preferences: {retrieved_by_id}")

    # 4. Test update_preferences and re-normalization
    print("\nStep 4: Updating preferences with new weights (0.5, 0.0, 0.5)")
    retrieved_by_id["atmosphere_weight"] = 0.5
    retrieved_by_id["budget_weight"] = 0.0
    retrieved_by_id["transport_weight"] = 0.5
    
    updated = update_preferences(retrieved_by_id)
    es.indices.refresh(index="fan_preferences")

    print(f"Updated preferences: {updated}")
    
    total_weights_updated = updated["atmosphere_weight"] + updated["budget_weight"] + updated["transport_weight"]
    assert abs(total_weights_updated - 1.0) < 1e-9
    assert updated["atmosphere_weight"] == 0.5
    assert updated["budget_weight"] == 0.0
    assert updated["transport_weight"] == 0.5
    assert updated["_seq_no"] > created["_seq_no"], "Sequence number should have incremented"

    # 5. Test optimistic concurrency locking check
    print("\nStep 5: Testing optimistic concurrency locking failure on stale update")
    stale_pref = updated.copy()
    # Force stale sequence number
    stale_pref["_seq_no"] = created["_seq_no"]
    
    conflict_occurred = False
    try:
        update_preferences(stale_pref)
    except Exception as e:
        conflict_occurred = True
        print(f"Stale update conflict successfully detected: {e}")
    
    assert conflict_occurred, "Expected a conflict error on stale sequence number update"

    # 6. Test delete_preferences
    print("\nStep 6: Deleting preference doc")
    delete_preferences("pref-test-1")
    es.indices.refresh(index="fan_preferences")
    deleted_check = get_preferences("pref-test-1")
    assert deleted_check is None, "Preference should be deleted"
    print("Delete verification passed")

    print("\n--- FAN PREFERENCE SERVICE UNIT TESTS PASSED SUCCESSFULLY ---")

if __name__ == "__main__":
    run_tests()
