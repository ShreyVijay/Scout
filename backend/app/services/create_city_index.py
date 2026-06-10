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
    if es.indices.exists(index="cities"):
        es.indices.delete(index="cities")
        print("Deleted existing cities index")

    es.indices.create(
        index="cities",
        mappings={
            "properties": {
                "city": {
                    "type": "keyword"
                },
                "country": {
                    "type": "keyword"
                },
                "description": {
                    "type": "text"
                },
                "tags": {
                    "type": "keyword"
                },
                "daily_cost": {
                    "type": "integer"
                },
                "hotel_cost": {
                    "type": "integer"
                },
                "transport_cost": {
                    "type": "integer"
                },
                "food_cost": {
                    "type": "integer"
                },
                "atmosphere_score": {
                    "type": "integer"
                },
                "budget_score": {
                    "type": "integer"
                },
                "transport_score": {
                    "type": "integer"
                },
                "fan_zone_score": {
                    "type": "integer"
                },
                "created_at": {
                    "type": "date"
                }
            }
        }
    )
    print("Created cities index successfully")

if __name__ == "__main__":
    create_index()
