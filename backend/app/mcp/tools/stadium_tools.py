from app.mcp.elastic_client import get_elastic_client
from app.mcp.schemas import error_response, success_response
from app.services.stadium_search import (
    get_city_stadiums as service_get_city_stadiums,
    get_stadium as service_get_stadium
)


def get_stadium(stadium: str):
    try:
        return success_response(service_get_stadium(stadium))
    except Exception as exc:
        return error_response(exc)


def get_city_stadiums(city: str):
    try:
        return success_response(service_get_city_stadiums(city))
    except Exception as exc:
        return error_response(exc)


def search_stadiums(query: str, size: int = 10):
    try:
        es = get_elastic_client()
        result = es.search(
            index="stadiums",
            size=size,
            query={
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "description"
                                ],
                                "fuzziness": "AUTO"
                            }
                        },
                        {
                            "wildcard": {
                                "stadium": {
                                    "value": f"*{query}*",
                                    "boost": 3.0,
                                    "case_insensitive": True
                                }
                            }
                        },
                        {
                            "wildcard": {
                                "city": {
                                    "value": f"*{query}*",
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
        stadiums = [
            hit["_source"]
            for hit in result["hits"]["hits"]
        ]
        return success_response(
            stadiums,
            metadata={
                "source_index": "stadiums"
            }
        )
    except Exception as exc:
        return error_response(exc)
