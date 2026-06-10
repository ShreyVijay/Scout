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

def get_city(city_name):
    """Exact lookup by city keyword."""
    result = es.search(
        index="cities",
        size=1,
        query={
            "term": {
                "city": city_name
            }
        }
    )
    hits = result["hits"]["hits"]
    if not hits:
        return None
    return hits[0]["_source"]

def search_city(query_str):
    """Full-text search on city or description."""
    result = es.search(
        index="cities",
        query={
            "multi_match": {
                "query": query_str,
                "fields": ["city", "description"]
            }
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]

def search_by_tag(tag):
    """Search by tags keyword match."""
    result = es.search(
        index="cities",
        query={
            "term": {
                "tags": tag
            }
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]

def get_all_cities():
    """Retrieve all cities, up to 100."""
    result = es.search(
        index="cities",
        size=100,
        query={
            "match_all": {}
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]
