import time
from app.services.event_store import (
    save_event,
    get_next_unprocessed_event,
    mark_event_processed
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

# Clean match_events index for test purity
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

# Test 1: Ingesting events in order and checking retrieval
print("Test 1: Ingesting events and checking queue order")
# Use specific event times to control order
time_a = "2026-06-10T10:00:00Z"
time_b = "2026-06-10T10:05:00Z"
time_c = "2026-06-10T10:10:00Z"

# Save in non-sequential order to test queue sorting
save_event("Egypt", "advanced", "round_of_16", "quarter_final", event_time=time_b)
save_event("Egypt", "advanced", "group_stage", "round_of_16", event_time=time_a)
save_event("Egypt", "advanced", "quarter_final", "semi_final", event_time=time_c)

# Refresh index to ensure immediate search visibility
es.indices.refresh(index="match_events")

# Retrieve next unprocessed - should be time_a
ev1 = get_next_unprocessed_event("Egypt")
print("First retrieved event (expected group_stage -> round_of_16):")
print(f"From: {ev1['from_stage']}, To: {ev1['to_stage']}, Time: {ev1['event_time']}")

# Mark first processed
mark_event_processed(ev1["_event_id"])
# Refresh index to ensure immediate search visibility
es.indices.refresh(index="match_events")

# Retrieve next - should be time_b
ev2 = get_next_unprocessed_event("Egypt")
print("Second retrieved event (expected round_of_16 -> quarter_final):")
print(f"From: {ev2['from_stage']}, To: {ev2['to_stage']}, Time: {ev2['event_time']}")

# Mark second processed
mark_event_processed(ev2["_event_id"])
es.indices.refresh(index="match_events")

# Retrieve next - should be time_c
ev3 = get_next_unprocessed_event("Egypt")
print("Third retrieved event (expected quarter_final -> semi_final):")
print(f"From: {ev3['from_stage']}, To: {ev3['to_stage']}, Time: {ev3['event_time']}")

# Test 2: Duplicate protection
print("\nTest 2: Duplicate protection test")
# Save event A with the same timestamp again
save_event("Egypt", "advanced", "group_stage", "round_of_16", event_time=time_a)
es.indices.refresh(index="match_events")

# Search all documents for Egypt (including processed ones)
result = es.search(
    index="match_events",
    query={"term": {"team": "Egypt"}}
)
print(f"Total documents in index for Egypt (expected 3): {result['hits']['total']['value']}")