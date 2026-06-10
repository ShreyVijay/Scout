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

def load_cities():
    # Construct paths relative to backend directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path_facts = os.path.join(base_dir, "data", "cities.json")
    file_path_scores = os.path.join(base_dir, "data", "city_scores.json")

    with open(file_path_facts, "r") as f:
        cities_facts = json.load(f)

    with open(file_path_scores, "r") as f:
        cities_scores = json.load(f)

    # Convert scores to a lookup dictionary by city name
    scores_lookup = {item["city"]: item for item in cities_scores}

    count = 0
    for city_doc in cities_facts:
        city_name = city_doc["city"]
        score_data = scores_lookup.get(city_name, {})

        # Merge facts and Scout intelligence scores
        city_doc["atmosphere_score"] = score_data.get("atmosphere_score", 0.0)
        city_doc["budget_score"] = score_data.get("budget_score", 0.0)
        city_doc["transport_score"] = score_data.get("transport_score", 0.0)
        city_doc["fan_zone_score"] = score_data.get("fan_zone_score", 0.0)
        
        city_doc["created_at"] = datetime.utcnow().isoformat()
        
        # Use city name as ID to prevent duplicates
        doc_id = city_name
        
        es.index(
            index="cities",
            id=doc_id,
            document=city_doc
        )
        count += 1

    # Refresh index
    es.indices.refresh(index="cities")
    print(f"Successfully loaded and merged {count} cities into cities index")

if __name__ == "__main__":
    load_cities()
