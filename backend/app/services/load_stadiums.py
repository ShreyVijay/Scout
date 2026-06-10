import os
import json
from datetime import datetime
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

def load_stadiums():
    # Construct paths relative to backend directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "stadiums.json")

    with open(file_path, "r") as f:
        stadiums = json.load(f)

    count = 0
    for stadium_doc in stadiums:
        stadium_doc["created_at"] = datetime.utcnow().isoformat()
        
        # Use stadium name as ID to prevent duplicates
        doc_id = stadium_doc["stadium"]
        
        es.index(
            index="stadiums",
            id=doc_id,
            document=stadium_doc
        )
        count += 1

    # Refresh index
    es.indices.refresh(index="stadiums")
    print(f"Successfully loaded {count} stadiums into stadiums index")

if __name__ == "__main__":
    load_stadiums()
