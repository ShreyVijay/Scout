from app.services.mission_budget_service import (
    integrate_mission_budget
)

def test_integration():

    print(
        "--- Testing Mission Budget Integration ---"
    )

    egypt_mission = {
        "mission_id": "egypt-test-integration",
        "team": "Egypt",
        "budget": 2500,
        "itinerary": [
            {
                "city": "New York",
                "stadium": "MetLife Stadium",
                "date": "2026-06-15"
            },
            {
                "city": "Dallas",
                "stadium": "AT&T Stadium",
                "date": "2026-06-20"
            },
            {
                "city": "Los Angeles",
                "stadium": "SoFi Stadium",
                "date": "2026-06-25"
            }
        ]
    }

    result = integrate_mission_budget(
        egypt_mission,
        spent_budget=200
    )

    assert result["budget"] == 2500

    intel = result["budget_intelligence"]

    assert intel["total_budget"] == 2500
    assert intel["spent_budget"] == 200
    assert intel["estimated_cost"] == 670

    assert (
        intel["projected_remaining_budget"]
        == 1630
    )

    assert intel["risk_level"] == "LOW"

    print(
        "Mission Budget Integration tests passed successfully!"
    )

if __name__ == "__main__":
    test_integration()