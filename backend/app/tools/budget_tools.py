from app.services.mission_store import get_latest_mission
from app.services.budget_intelligence import get_budget_intelligence
from app.services.budget_profile_service import get_budget_profile
from app.services.budget_calculator import calculate_estimated_cost

def get_budget_status(team: str):
    """
    Returns the budget status (total, spent, remaining, and risk level) for a team's mission.
    """
    mission = get_latest_mission(team)
    if not mission:
        return f"No mission found for team {team}."

    profile = get_budget_profile(mission["mission_id"])
    spent = profile.get("spent_budget", 0) if profile else 0

    intel = get_budget_intelligence(mission, spent_budget=spent)
    return intel

def estimate_trip_cost(team: str):
    """
    Returns estimated trip cost for the current itinerary of a team's mission.
    """
    mission = get_latest_mission(team)
    if not mission:
        return f"No mission found for team {team}."

    calc = calculate_estimated_cost(mission)
    return calc
