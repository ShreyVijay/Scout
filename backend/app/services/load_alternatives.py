# backend/app/services/load_alternatives.py

import json
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

with open("../datasets/alternative_routes.json", "r") as f:
    routes = json.load(f)

for route in routes:
    es.index(
        index="alternative_routes",
        document=route
    )

print(f"Loaded {len(routes)} alternative routes.")