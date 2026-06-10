from app.services.planner import build_trip

def generate_trip(team: str):
    """
    Generates a travel itinerary for a team.
    """
    return build_trip(team)