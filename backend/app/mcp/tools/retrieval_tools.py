from app.mcp.schemas import error_response, success_response
from app.services.alternative_search import get_alternative_routes
from app.services.semantic_candidate_service import (
    retrieve_city_candidates as service_retrieve_city_candidates,
    retrieve_stadium_candidates as service_retrieve_stadium_candidates
)


def _with_metadata(candidate, candidate_source, source_index):
    enriched = candidate.copy()
    enriched["candidate_source"] = candidate_source
    enriched["metadata"] = {
        **enriched.get("metadata", {}),
        "source_index": source_index
    }
    return enriched


def retrieve_city_candidates(query: str, size: int = 5):
    try:
        candidates = service_retrieve_city_candidates(
            query,
            size=size
        )
        candidates = [
            _with_metadata(candidate, "semantic_city", "cities")
            for candidate in candidates
        ]
        return success_response(candidates)
    except Exception as exc:
        return error_response(exc)


def retrieve_stadium_candidates(query: str, size: int = 5):
    try:
        candidates = service_retrieve_stadium_candidates(
            query,
            size=size
        )
        candidates = [
            _with_metadata(candidate, "semantic_stadium", "stadiums")
            for candidate in candidates
        ]
        return success_response(candidates)
    except Exception as exc:
        return error_response(exc)


def retrieve_route_candidates(size: int = 10):
    try:
        routes = get_alternative_routes()[:size]
        routes = [
            _with_metadata(route, "route", "alternative_routes")
            for route in routes
        ]
        return success_response(routes)
    except Exception as exc:
        return error_response(exc)
