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

def search_matches(team: str):

    result = es.search(
        index="tournament_matches",
        query={
            "match": {
                "team": team
            }
        }
    )

    matches = []

    for hit in result["hits"]["hits"]:
        matches.append(hit["_source"])

    return matches