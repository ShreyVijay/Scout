# app/services/reset_missions.py

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

if es.indices.exists(index="missions"):
    es.indices.delete(index="missions")
    print("Deleted missions index")

es.indices.create(
    index="missions",
    mappings={
        "properties": {
            "mission_id": {
                "type": "keyword"
            },
            "team": {
                "type": "keyword"
            },
            "budget": {
                "properties": {
                    "total_budget": {"type": "integer"},
                    "spent_budget": {"type": "integer"},
                    "estimated_cost": {"type": "integer"},
                    "remaining_budget": {"type": "integer"},
                    "risk_level": {"type": "keyword"}
                }
            },
            "travel_style": {
                "type": "keyword"
            },
            "objective": {
                "type": "text"
            },
            "mission_state": {
                "type": "keyword"
            },
            "tournament_state": {
                "type": "keyword"
            },
            "requires_replanning": {
                "type": "boolean"
            },
            "created_at": {
                "type": "date"
            },
            "updated_at": {
                "type": "date"
            },
            "itinerary": {
                "type": "nested",
                "properties": {
                    "city": {
                        "type": "keyword"
                    },
                    "stadium": {
                        "type": "text"
                    },
                    "date": {
                        "type": "date"
                    }
                }
            },
            "state_history": {
                "type": "nested",
                "properties": {
                    "state_type": {
                        "type": "keyword"
                    },
                    "from": {
                        "type": "keyword"
                    },
                    "to": {
                        "type": "keyword"
                    },
                    "timestamp": {
                        "type": "date"
                    }
                }
            }
        }
    }
)

print("Created missions index")