from app.services.budget_calculator import calculate_estimated_cost
from app.services.budget_risk_engine import calculate_budget_risk

def get_budget_intelligence(mission, spent_budget=0):

    budget_field = mission.get("budget", 0)

    if isinstance(budget_field, dict):
        total_budget = budget_field.get("total_budget", 0)
    else:
        total_budget = budget_field

    estimated_cost = calculate_estimated_cost(
        mission
    )["estimated_cost"]

    projected_remaining_budget = (
        total_budget
        - spent_budget
        - estimated_cost
    )

    projected_remaining_budget = max(
        0,
        projected_remaining_budget
    )

    risk_level = calculate_budget_risk(
        total_budget,
        projected_remaining_budget
    )["risk_level"]

    return {
        "total_budget": total_budget,
        "spent_budget": spent_budget,
        "estimated_cost": estimated_cost,
        "projected_remaining_budget": projected_remaining_budget,
        "risk_level": risk_level
    }