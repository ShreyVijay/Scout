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

if es.indices.exists(index="match_events"):
    es.indices.delete(index="match_events")
    print("Deleted match_events index")

es.indices.create(
    index="match_events",
    mappings={
        "properties": {
            "team": {
                "type": "keyword"
            },
            "event_type": {
                "type": "keyword"
            },
            "from_stage": {
                "type": "keyword"
            },
            "to_stage": {
                "type": "keyword"
            },
            "event_time": {
                "type": "date"
            },
            "processed": {
                "type": "boolean"
            }
        }
    }
)

print("match_events ready")