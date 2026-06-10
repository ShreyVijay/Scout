from app.services.mission_city_service import get_mission_cities_intelligence

def test_mission_city_service_all():
    print("--- Testing Mission City Integration Service ---")

    # Mock mission document with itinerary
    mock_mission = {
        "mission_id": "test-mission-123",
        "team": "Egypt",
        "itinerary": [
            {"city": "New York", "stadium": "MetLife Stadium", "date": "2026-06-15"},
            {"city": "Dallas", "stadium": "AT&T Stadium", "date": "2026-06-20"},
            {"city": "Los Angeles", "stadium": "SoFi Stadium", "date": "2026-06-25"},
            {"city": "New York", "stadium": "MetLife Stadium", "date": "2026-06-30"} # Duplicate city in itinerary
        ]
    }

    print("Running itinerary resolution...")
    result = get_mission_cities_intelligence(mock_mission)
    assert result["mission_id"] == "test-mission-123"
    
    # We expect exactly 3 unique cities (New York, Dallas, Los Angeles)
    assert len(result["cities"]) == 3
    city_names = [c["city"] for c in result["cities"]]
    print(f"Aggregated unique itinerary cities: {city_names}")
    assert city_names == ["New York", "Dallas", "Los Angeles"]

    # Verify nested details
    nyc_intel = result["cities"][0]
    assert nyc_intel["city"] == "New York"
    assert len(nyc_intel["stadiums"]) == 1
    assert nyc_intel["stadiums"][0]["stadium"] == "MetLife Stadium"
    print("Mission itinerary resolution verified.")
    print("Mission City Service Tests Passed Successfully!\n")

if __name__ == "__main__":
    test_mission_city_service_all()
