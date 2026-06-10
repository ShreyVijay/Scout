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
    if es.indices.exists(index="stadiums"):
        es.indices.delete(index="stadiums")
        print("Deleted existing stadiums index")

    es.indices.create(
        index="stadiums",
        mappings={
            "properties": {
                "stadium": {
                    "type": "keyword"
                },
                "city": {
                    "type": "keyword"
                },
                "country": {
                    "type": "keyword"
                },
                "capacity": {
                    "type": "integer"
                },
                "description": {
                    "type": "text"
                },
                "atmosphere_score": {
                    "type": "integer"
                },
                "transport_score": {
                    "type": "integer"
                },
                "created_at": {
                    "type": "date"
                }
            }
        }
    )
    print("Created stadiums index successfully")

if __name__ == "__main__":
    create_index()
