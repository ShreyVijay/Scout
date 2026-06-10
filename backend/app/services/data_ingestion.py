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

def ingest_matches(file_path):

    with open(file_path, "r") as f:
        matches = json.load(f)

    count = 0

    for match in matches:

        es.index(
            index="tournament_matches",
            document=match
        )

        count += 1

    return count