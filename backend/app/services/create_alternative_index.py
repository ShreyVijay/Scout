# backend/app/services/create_alternative_index.py

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

if not es.indices.exists(index="alternative_routes"):
    es.indices.create(index="alternative_routes")
    print("Created alternative_routes index")
else:
    print("alternative_routes already exists")