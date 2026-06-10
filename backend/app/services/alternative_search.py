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

def get_alternative_routes():

    result = es.search(
        index="alternative_routes",
        query={
            "match_all": {}
        }
    )

    routes = []

    for hit in result["hits"]["hits"]:
        routes.append(hit["_source"])

    return routes