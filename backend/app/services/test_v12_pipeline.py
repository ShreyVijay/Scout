import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from app.services.mission_service import create_mission
from app.services.mission_store import get_latest_mission, update_mission
from app.services.mission_state_service import update_mission_state
from app.services.event_store import save_event, get_next_unprocessed_event
from app.services.tournament_evaluator import process_latest_event

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def run_integration_test():
    print("--- STARTING FULL INTEGRATION PIPELINE TEST ---")

    # 1. Clean indices for test purity
    print("\nStep 1: Recreating indices for clean test environment")
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

    if es.indices.exists(index="match_events"):
        es.indices.delete(index="match_events")
    es.indices.create(
        index="match_events",
        mappings={
            "properties": {
                "team": {"type": "keyword"},
                "event_type": {"type": "keyword"},
                "from_stage": {"type": "keyword"},
                "to_stage": {"type": "keyword"},
                "event_time": {"type": "date"},
                "processed": {"type": "boolean"}
            }
        }
    )
    es.indices.refresh(index="missions")
    es.indices.refresh(index="match_events")

    # 2. Create Mission
    print("\nStep 2: Creating planned mission for Egypt")
    mission = create_mission(
        team="Egypt",
        budget=3000,
        travel_style="Budget",
        objective="Support Egypt in the tournament"
    )
    es.indices.refresh(index="missions")
    print(f"Created Mission State: {mission['mission_state']}, Tournament State: {mission['tournament_state']}")

    # 3. Transition Mission to Active
    print("\nStep 3: Advancing mission state to 'active'")
    mission = get_latest_mission("Egypt")
    mission = update_mission_state(mission, "active")
    update_mission(mission)
    es.indices.refresh(index="missions")
    mission = get_latest_mission("Egypt")
    print(f"Updated Mission State: {mission['mission_state']}, Tournament State: {mission['tournament_state']}")

    # 4. Inject Events in Mixed (Out of Order) Sequence
    print("\nStep 4: Injecting events in reverse chronological order to test queue sorting")
    
    # Chronological timestamps
    time_1_r16 = "2026-06-10T12:00:00Z"
    time_2_qf = "2026-06-10T12:05:00Z"
    time_3_sf = "2026-06-10T12:10:00Z"
    time_4_elim = "2026-06-10T12:15:00Z"

    # Save to ES out of chronological order
    print("Saving event: semi_final -> eliminated (latest)...")
    save_event("Egypt", "advanced", "semi_final", "eliminated", event_time=time_4_elim)

    print("Saving event: group_stage -> round_of_16 (earliest)...")
    save_event("Egypt", "advanced", "group_stage", "round_of_16", event_time=time_1_r16)

    print("Saving event: quarter_final -> semi_final (third)...")
    save_event("Egypt", "advanced", "quarter_final", "semi_final", event_time=time_3_sf)

    print("Saving event: round_of_16 -> quarter_final (second)...")
    save_event("Egypt", "advanced", "round_of_16", "quarter_final", event_time=time_2_qf)

    # Refresh index
    es.indices.refresh(index="match_events")
    print("Index match_events refreshed.")

    # 5. Process events sequentially and assert intermediate states
    print("\nStep 5: Processing events from queue and verifying order")
    
    expected_transitions = [
        ("group_stage", "round_of_16"),
        ("round_of_16", "quarter_final"),
        ("quarter_final", "semi_final"),
        ("semi_final", "eliminated")
    ]

    for index, (expected_from, expected_to) in enumerate(expected_transitions, 1):
        print(f"\n--- Processing Event {index} ---")
        
        # Verify the next event in queue is correct BEFORE calling evaluator
        next_event = get_next_unprocessed_event("Egypt")
        if not next_event:
            raise Exception("Expected unprocessed event, but queue is empty!")
            
        print(f"Next unprocessed event in queue: {next_event['from_stage']} -> {next_event['to_stage']} at {next_event['event_time']}")
        assert next_event["from_stage"] == expected_from, f"Expected {expected_from}, got {next_event['from_stage']}"
        assert next_event["to_stage"] == expected_to, f"Expected {expected_to}, got {next_event['to_stage']}"

        # Evaluate/Process the event
        mission = process_latest_event("Egypt")
        es.indices.refresh(index="missions")
        es.indices.refresh(index="match_events")
        
        # Reload latest mission state
        mission = get_latest_mission("Egypt")
        print(f"Mission updated. Current Tournament State: {mission['tournament_state']}, Mission State: {mission['mission_state']}")
        assert mission["tournament_state"] == expected_to, f"Expected tournament state to be {expected_to}, got {mission['tournament_state']}"

    # 6. Verify final outputs and state history transitions count
    print("\nStep 6: Verifying final states and history log")
    mission = get_latest_mission("Egypt")
    
    # Print the full state history
    print("\nMission State History:")
    for h in mission["state_history"]:
        print(f"  - Type: {h['state_type']}, From: {h['from']}, To: {h['to']}, Timestamp: {h['timestamp']}")

    # Verification assertions
    tournament_transitions = [h for h in mission["state_history"] if h["state_type"] == "tournament"]
    mission_transitions = [h for h in mission["state_history"] if h["state_type"] == "mission"]

    print(f"\nTournament transition count: {len(tournament_transitions)}")
    print(f"Mission transition count: {len(mission_transitions)}")
    
    assert len(tournament_transitions) == 4, f"Expected exactly 4 tournament transitions, got {len(tournament_transitions)}"
    assert mission["tournament_state"] == "eliminated", f"Expected tournament state 'eliminated', got {mission['tournament_state']}"
    
    # Egypt is active -> tournament semi_final -> eliminated resolving to replanning/monitoring
    # Let's check: 
    # Transition 1: group_stage -> round_of_16 (no resolve trigger mapping for R16, remains active)
    # Transition 2: round_of_16 -> quarter_final (no resolver mapping for QF on active, but wait, (quarter_final, active) -> monitoring!)
    # Transition 3: quarter_final -> semi_final ((semi_final, active) -> monitoring, or if monitoring, remains monitoring)
    # Transition 4: semi_final -> eliminated ((eliminated, monitoring) -> replanning)
    print(f"Final Mission State: {mission['mission_state']}")
    assert mission["mission_state"] == "replanning", f"Expected final mission state 'replanning', got {mission['mission_state']}"

    print("\n--- ALL PIPELINE CHECKS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_integration_test()
