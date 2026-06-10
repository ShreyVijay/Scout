from app.services.alternative_search import get_alternative_routes
from app.services.candidate_merge_service import merge_candidates
from app.services.semantic_candidate_service import (
    retrieve_city_candidates,
    retrieve_stadium_candidates
)


def _build_retrieval_query(mission):
    team = mission.get("team")
    travel_style = mission.get("travel_style")
    objective = mission.get("objective")

    if team:
        return f"{team} football atmosphere"
    if travel_style:
        return travel_style
    return objective


def get_candidates(mission):
    """
    Retrieves raw replanning candidates from alternative routes and semantic
    retrieval sources.
    """
    routes = get_alternative_routes()

    route_candidates = [
        {
            "city": route["city"],
            "match": route["match"],
            "reason": route["reason"],
            "candidate_source": "route"
        }
        for route in routes
    ]

    query = _build_retrieval_query(mission)
    semantic_city_candidates = []
    semantic_stadium_candidates = []

    if query:
        semantic_city_candidates = retrieve_city_candidates(
            query,
            size=5
        )[:5]
        semantic_stadium_candidates = retrieve_stadium_candidates(
            query,
            size=5
        )[:5]

    return merge_candidates(
        route_candidates,
        semantic_city_candidates,
        semantic_stadium_candidates
    )
