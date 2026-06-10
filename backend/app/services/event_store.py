import os
import hashlib
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def save_event(
    team,
    event_type,
    from_stage,
    to_stage,
    event_time=None
):
    if event_time is None:
        event_time = datetime.utcnow().isoformat()

    # Generate a deterministic ID based on team, from_stage, to_stage, and event_time to protect against duplicates
    payload = f"{team}_{from_stage}_{to_stage}_{event_time}"
    event_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    event = {
        "team": team,
        "event_type": event_type,
        "from_stage": from_stage,
        "to_stage": to_stage,
        "event_time": event_time,
        "processed": False
    }

    return es.index(
        index="match_events",
        id=event_id,
        document=event
    )

def get_next_unprocessed_event(team):
    result = es.search(
        index="match_events",
        size=1,
        query={
            "bool": {
                "must": [
                    {"term": {"team": team}},
                    {"term": {"processed": False}}
                ]
            }
        },
        sort=[
            {
                "event_time": {
                    "order": "asc"
                }
            }
        ]
    )

    hits = result["hits"]["hits"]

    if not hits:
        return None

    event = hits[0]["_source"]
    event["_event_id"] = hits[0]["_id"]

    return event

def mark_event_processed(event_id):
    return es.update(
        index="match_events",
        id=event_id,
        doc={
            "processed": True
        }
    )

# @deprecated: Use get_next_unprocessed_event instead.
def get_latest_event(team):
    result = es.search(
        index="match_events",
        size=1,
        sort=[
            {
                "event_time": {
                    "order": "desc"
                }
            }
        ],
        query={
            "term": {
                "team": team
            }
        }
    )

    hits = result["hits"]["hits"]

    if not hits:
        return None

    return hits[0]["_source"]