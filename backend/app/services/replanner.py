from app.services.alternative_search import get_alternative_routes
from app.services.mission_store import get_latest_mission

def rebuild_trip(team: str):

    mission = get_latest_mission(team)

    routes = get_alternative_routes()

    travel_style = mission["travel_style"]

    best_route = None

    for route in routes:

        if route["type"] == travel_style:
            best_route = route
            break

    if best_route is None:
        best_route = routes[0]

    return {
        "team": team,
        "travel_style": travel_style,
        "old_itinerary": mission["itinerary"],
        "new_destination": best_route["city"],
        "match": best_route["match"],
        "reason": best_route["reason"],
        "status": "replanned"
    }