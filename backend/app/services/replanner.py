from app.services.replanning_engine import run_replanning
from app.services.mission_store import get_latest_mission

def rebuild_trip(team: str):
    """
    Rebuilds the trip for the team using the new modular replanning engine.
    Maintains backward compatibility with the original rebuild_trip signature and output.
    """
    mission = get_latest_mission(team)
    result = run_replanning(mission)
    rec = result.get("recommendation")

    if not rec:
        return {
            "team": team,
            "travel_style": mission.get("travel_style"),
            "old_itinerary": mission.get("itinerary"),
            "new_destination": None,
            "match": None,
            "reason": None,
            "status": "replanned"
        }

    return {
        "team": team,
        "travel_style": mission.get("travel_style"),
        "old_itinerary": mission.get("itinerary"),
        "new_destination": rec["city"],
        "match": rec["match"],
        "reason": rec["reason"],
        "status": "replanned"
    }