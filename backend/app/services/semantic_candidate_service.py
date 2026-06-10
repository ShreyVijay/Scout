# backend/app/services/semantic_candidate_service.py

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


def retrieve_city_candidates(query_text, size=10):
    """
    Searches the cities index using a bool query:
    - multi_match on description (text field)
    - wildcard on city name (keyword field)
    - terms on tags (keyword field)

    Returns raw retrieval candidates only.
    No scoring. No ranking. No filtering.
    """

    result = es.search(
        index="cities",
        size=size,
        query={
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query_text,
                            "fields": [
                                "description^2",
                                "country"
                            ],
                            "type": "best_fields",
                            "fuzziness": "AUTO"
                        }
                    },
                    {
                        "wildcard": {
                            "city": {
                                "value": f"*{query_text}*",
                                "boost": 3.0,
                                "case_insensitive": True
                            }
                        }
                    },
                    {
                        "terms": {
                            "tags": query_text.split(),
                            "boost": 1.5
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        }
    )

    candidates = []

    for hit in result["hits"]["hits"]:

        source = hit["_source"]

        candidates.append({
            "candidate_type": "city",
            "city": source.get("city"),
            "country": source.get("country"),
            "description": source.get(
                "description"
            ),
            "tags": source.get("tags", []),
            "retrieval_score": hit["_score"]
        })

    return candidates


def retrieve_stadium_candidates(
    query_text,
    size=10
):
    """
    Searches the stadiums index using a bool query:
    - multi_match on description (text field)
    - wildcard on stadium name (keyword field)
    - wildcard on city (keyword field)

    Returns raw retrieval candidates only.
    No scoring. No ranking. No filtering.
    """

    result = es.search(
        index="stadiums",
        size=size,
        query={
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query_text,
                            "fields": [
                                "description^2",
                                "country"
                            ],
                            "type": "best_fields",
                            "fuzziness": "AUTO"
                        }
                    },
                    {
                        "wildcard": {
                            "stadium": {
                                "value": f"*{query_text}*",
                                "boost": 3.0,
                                "case_insensitive": True
                            }
                        }
                    },
                    {
                        "wildcard": {
                            "city": {
                                "value": f"*{query_text}*",
                                "boost": 2.0,
                                "case_insensitive": True
                            }
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        }
    )

    candidates = []

    for hit in result["hits"]["hits"]:

        source = hit["_source"]

        candidates.append({
            "candidate_type": "stadium",
            "stadium": source.get("stadium"),
            "city": source.get("city"),
            "country": source.get("country"),
            "capacity": source.get("capacity"),
            "description": source.get(
                "description"
            ),
            "retrieval_score": hit["_score"]
        })

    return candidates

