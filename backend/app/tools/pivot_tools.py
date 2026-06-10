from app.services.pivot_engine import evaluate_trip

def check_team_status(team: str):
    """
    Checks whether a team is still active
    and whether itinerary replanning is needed.
    """

    return evaluate_trip(team)