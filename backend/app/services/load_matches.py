import json
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

with open("../datasets/egypt_matches.json", "r") as f:
    matches = json.load(f)

for match in matches:
    es.index(
        index="tournament_matches",
        document=match
    )

print("Egypt matches loaded successfully")