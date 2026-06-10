from app.services.budget_intelligence import get_budget_intelligence

def test_intelligence():
    print("--- Testing Budget Intelligence ---")

    egypt_mission = {
        "mission_id": "egypt-test-intel",
        "team": "Egypt",
        "budget": 2500,
        "itinerary": [
            {"city": "New York", "stadium": "MetLife Stadium", "date": "2026-06-15"},
            {"city": "Dallas", "stadium": "AT&T Stadium", "date": "2026-06-20"},
            {"city": "Los Angeles", "stadium": "SoFi Stadium", "date": "2026-06-25"}
        ]
    }

    # Case 1: spent = 0 -> remaining = 2500 (100% of 2500 -> LOW risk)
    intel1 = get_budget_intelligence(egypt_mission, spent_budget=0)
    assert intel1["total_budget"] == 2500
    assert intel1["spent_budget"] == 0
    assert intel1["estimated_cost"] == 670
    assert intel1["remaining_budget"] == 2500
    assert intel1["risk_level"] == "LOW"

    # Case 2: spent = 1500 -> remaining = 1000 (40% of 2500 -> MEDIUM risk)
    intel2 = get_budget_intelligence(egypt_mission, spent_budget=1500)
    assert intel2["remaining_budget"] == 1000
    assert intel2["risk_level"] == "MEDIUM"

    # Case 3: spent = 2100 -> remaining = 400 (16% of 2500 -> HIGH risk)
    intel3 = get_budget_intelligence(egypt_mission, spent_budget=2100)
    assert intel3["remaining_budget"] == 400
    assert intel3["risk_level"] == "HIGH"

    print("Budget Intelligence tests passed successfully!\n")

if __name__ == "__main__":
    test_intelligence()
