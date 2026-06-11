from contracts.base import ScoutDTO


class BudgetResponse(ScoutDTO):
    total_budget: float = 0
    spent_budget: float = 0
    estimated_cost: float = 0
    projected_remaining_budget: float = 0
    risk_level: str = "UNKNOWN"
