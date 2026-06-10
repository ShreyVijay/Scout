from app.services.budget_intelligence import (
    get_budget_intelligence
)

def integrate_mission_budget(
    mission,
    spent_budget=0
):

    if not mission:
        return None

    intel = get_budget_intelligence(
        mission,
        spent_budget
    )
    mission["budget_intelligence"] = intel

    if isinstance(mission.get("budget"), dict):
        mission["budget"]["spent_budget"] = intel["spent_budget"]
        mission["budget"]["estimated_cost"] = intel["estimated_cost"]
        mission["budget"]["remaining_budget"] = intel["total_budget"] - intel["spent_budget"]
        mission["budget"]["risk_level"] = intel["risk_level"]

    return mission