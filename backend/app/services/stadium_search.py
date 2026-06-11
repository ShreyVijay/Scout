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

def get_stadium(stadium_name):
    """Exact lookup by stadium keyword."""
    result = es.search(
        index="stadiums",
        size=1,
        query={
            "term": {
                "stadium": stadium_name
            }
        }
    )
    hits = result["hits"]["hits"]
    if not hits:
        return None
    return hits[0]["_source"]

def get_city_stadiums(city_name):
    """Filter stadiums by city keyword."""
    result = es.search(
        index="stadiums",
        size=50,
        query={
            "term": {
                "city": city_name
            }
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]


def search_stadiums(query_str, size=10):
    """Full-text stadium search. Elasticsearch access remains in the service layer."""
    result = es.search(
        index="stadiums",
        size=size,
        query={
            "multi_match": {
                "query": query_str,
                "fields": ["stadium^3", "city^2", "description"],
                "fuzziness": "AUTO",
            }
        },
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]

def get_all_stadiums():
    """Retrieve all stadiums, up to 100."""
    result = es.search(
        index="stadiums",
        size=100,
        query={
            "match_all": {}
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]
