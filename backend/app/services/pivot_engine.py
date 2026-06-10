from app.services.team_status import get_team_status
from app.services.replanner import rebuild_trip

def evaluate_trip(team: str):

    status = get_team_status(team)

    if status == "eliminated":

        return rebuild_trip(team)

    return {
        "team": team,
        "status": "active",
        "message": f"{team} is still active."
    }