from app.services.budget_calculator import calculate_estimated_cost

def test_calculator():
    print("--- Testing Budget Calculator ---")

    # Egypt Itinerary mockup
    egypt_mission = {
        "mission_id": "egypt-test-1",
        "team": "Egypt",
        "itinerary": [
            {"city": "New York", "stadium": "MetLife Stadium", "date": "2026-06-15"},
            {"city": "Dallas", "stadium": "AT&T Stadium", "date": "2026-06-20"},
            {"city": "Los Angeles", "stadium": "SoFi Stadium", "date": "2026-06-25"}
        ]
    }

    result = calculate_estimated_cost(egypt_mission)
    print(f"Calculated Estimated Cost: {result['estimated_cost']}")
    # NY (180+40+30=250) + Dallas (120+35+25=180) + LA (170+45+25=240) = 670
    assert result["estimated_cost"] == 670, f"Expected 670, got {result['estimated_cost']}"
    print("Budget Calculator tests passed successfully!\n")

if __name__ == "__main__":
    test_calculator()
