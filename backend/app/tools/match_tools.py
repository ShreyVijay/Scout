from app.services.search_service import search_matches
from app.services.planner import build_trip

def get_team_matches(team: str):
    """
    Returns all matches for a team.
    """
    return search_matches(team)
