# backend/app/services/create_indices.py

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

indices = [
    "tournament_matches",
    "stadium_intelligence",
    "city_intelligence",
    "ticket_market"
]

for idx in indices:
    if not es.indices.exists(index=idx):
        es.indices.create(index=idx)
        print(f"Created: {idx}")
    else:
        print(f"Already exists: {idx}")