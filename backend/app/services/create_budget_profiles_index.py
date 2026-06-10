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
    if es.indices.exists(index="budget_profiles"):
        es.indices.delete(index="budget_profiles")
        print("Deleted existing budget_profiles index")

    es.indices.create(
        index="budget_profiles",
        mappings={
            "properties": {
                "profile_id": {
                    "type": "keyword"
                },
                "mission_id": {
                    "type": "keyword"
                },
                "team": {
                    "type": "keyword"
                },
                "total_budget": {
                    "type": "integer"
                },
                "spent_budget": {
                    "type": "integer"
                },
                "remaining_budget": {
                    "type": "integer"
                },
                "risk_level": {
                    "type": "keyword"
                },
                "created_at": {
                    "type": "date"
                },
                "updated_at": {
                    "type": "date"
                }
            }
        }
    )
    print("Created budget_profiles index successfully")

if __name__ == "__main__":
    create_index()
