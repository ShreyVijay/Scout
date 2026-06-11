from app.services.planner import build_trip
from app.services.mission_store import save_mission
from app.services.mission_store import get_latest_mission, get_mission_history
from contracts.mission import MissionResponse
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
        "tournament_state": "GROUP_STAGE",
        "group": None,
        "group_position": None,
        "third_place_rank": None,
        "qualified": None,
        "round": "GROUP_STAGE",
        "state_history": []
    }

    save_mission(mission)

    import threading
    import time
    from datetime import datetime
    from app.services.mission_store import update_mission

    def simulate_elimination(mission_id, team_name):
        time.sleep(30)
        # Fetch the latest mission state
        m = get_latest_mission(team_name)
        if m and m.get("mission_id") == mission_id:
            m["tournament_state"] = "ELIMINATED"
            m["mission_state"] = "replanning_required"
            m["state_history"].append({
                "state": "ELIMINATED",
                "timestamp": datetime.utcnow().isoformat(),
                "reason": f"{team_name} eliminated in Round of 32"
            })
            update_mission(m)

    threading.Thread(target=simulate_elimination, args=(mission["mission_id"], team), daemon=True).start()

    return mission


def get_mission(team: str) -> MissionResponse | None:
    mission = get_latest_mission(team)
    return MissionResponse.model_validate(mission) if mission else None


def get_history(team: str, size: int = 20) -> list[MissionResponse]:
    return [
        MissionResponse.model_validate(mission)
        for mission in get_mission_history(team, size=size)
    ]
