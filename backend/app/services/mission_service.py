from app.services.planner import build_trip
from app.services.mission_store import save_mission
import uuid

def create_mission(
    team: str,
    budget: int,
    travel_style: str,
    objective: str
):

    itinerary = build_trip(team)

    mission = {
        
    "mission_id": str(uuid.uuid4()),

    "team": team,

    "budget": {
        "total_budget": budget,
        "spent_budget": 0,
        "estimated_cost": 0,
        "remaining_budget": budget,
        "risk_level": "LOW"
    },

    "travel_style": travel_style,

    "objective": objective,

    "itinerary": itinerary,

    "mission_state": "planned",

    "tournament_state": "group_stage",

    "state_history": []
}

    save_mission(mission)

    return mission