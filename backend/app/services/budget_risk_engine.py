def calculate_budget_risk(total_budget, remaining_budget):
    """
    Determine budget risk level based on remaining budget boundaries.
    """
    if total_budget <= 0:
        return {
            "risk_level": "HIGH"
        }

    ratio = remaining_budget / total_budget

    if ratio >= 0.50:
        risk = "LOW"
    elif ratio >= 0.20:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "risk_level": risk
    }
