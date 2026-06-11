from contracts.budget import BudgetResponse
from app.services.budget_intelligence import get_budget_intelligence
from app.services.mission_store import get_latest_mission


def get_budget(team: str) -> BudgetResponse | None:
    mission = get_latest_mission(team)
    if not mission:
        return None
    return BudgetResponse.model_validate(get_budget_intelligence(mission))
