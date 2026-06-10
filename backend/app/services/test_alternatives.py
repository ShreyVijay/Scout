# backend/app/services/test_alternatives.py

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

result = es.search(
    index="alternative_routes",
    query={
        "match_all": {}
    }
)

for hit in result["hits"]["hits"]:
    print(hit["_source"])