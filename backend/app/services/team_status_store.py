# app/services/team_status_store.py

import os
from datetime import datetime
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

def save_team_status(team, status):

    doc = {
        "team": team,
        "status": status,
        "updated_at": datetime.utcnow().isoformat()
    }

    es.index(
        index="team_progress",
        document=doc
    )

def get_latest_team_status(team):

    result = es.search(
        index="team_progress",
        size=1,
        sort=[
            {
                "updated_at": {
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