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

def load_alternatives():
    # Recreate index mapping if index doesn't exist
    if not es.indices.exists(index="alternative_routes"):
        es.indices.create(
            index="alternative_routes",
            mappings={
                "properties": {
                    "type": {"type": "keyword"},
                    "city": {"type": "keyword"},
                    "match": {"type": "keyword"},
                    "reason": {"type": "text"}
                }
            }
        )
        print("Created alternative_routes index")

    # Resolve alternative routes JSON file path cleanly
    current_dir = os.path.dirname(os.path.abspath(__file__)) # backend/app/services
    app_dir = os.path.dirname(current_dir) # backend/app
    backend_dir = os.path.dirname(app_dir) # backend
    scout_root = os.path.dirname(backend_dir) # Scout (root)
    file_path = os.path.join(scout_root, "datasets", "alternative_routes.json")

    with open(file_path, "r") as f:
        routes = json.load(f)

    for route in routes:
        # Use deterministic ID based on type and city to prevent duplicate appends
        doc_id = f"{route['type'].lower()}_{route['city'].lower().replace(' ', '_')}"
        es.index(
            index="alternative_routes",
            id=doc_id,
            document=route
        )

    es.indices.refresh(index="alternative_routes")
    print(f"Loaded {len(routes)} alternative routes cleanly.")

if __name__ == "__main__":
    load_alternatives()
