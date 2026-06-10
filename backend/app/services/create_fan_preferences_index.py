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

def create_index():
    if es.indices.exists(index="fan_preferences"):
        es.indices.delete(index="fan_preferences")
        print("Deleted existing fan_preferences index")

    es.indices.create(
        index="fan_preferences",
        mappings={
            "properties": {
                "preference_id": {"type": "keyword"},
                "mission_id": {"type": "keyword"},
                "team": {"type": "keyword"},
                "travel_style": {"type": "keyword"},
                "atmosphere_weight": {"type": "float"},
                "budget_weight": {"type": "float"},
                "transport_weight": {"type": "float"},
                "preference_version": {"type": "integer"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"}
            }
        }
    )
    print("Created fan_preferences index successfully")

if __name__ == "__main__":
    create_index()
