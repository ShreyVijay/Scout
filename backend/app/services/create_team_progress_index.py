# app/services/create_team_progress_index.py

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

if not es.indices.exists(index="team_progress"):
    es.indices.create(
        index="team_progress",
        mappings={
            "properties": {
                "team": {
                    "type": "keyword"
                },
                "status": {
                    "type": "keyword"
                },
                "updated_at": {
                    "type": "date"
                }
            }
        }
    )

print("team_progress ready")