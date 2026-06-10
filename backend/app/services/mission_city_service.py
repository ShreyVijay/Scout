from app.services.city_intelligence import get_city_intelligence

def get_mission_cities_intelligence(mission):
    """
    Extract and aggregate city intelligence for all cities in the mission's itinerary.
    """
    if not mission or "itinerary" not in mission:
        return {
            "mission_id": mission.get("mission_id") if mission else None,
            "cities": []
        }

    # Extract unique city names from the itinerary in order of appearance
    seen_cities = set()
    unique_cities = []
    for item in mission["itinerary"]:
        city_name = item.get("city")
        if city_name and city_name not in seen_cities:
            seen_cities.add(city_name)
            unique_cities.append(city_name)

    # Resolve intelligence for each city
    cities_intel = []
    for city in unique_cities:
        intel = get_city_intelligence(city)
        if intel:
            cities_intel.append(intel)

    return {
        "mission_id": mission.get("mission_id"),
        "cities": cities_intel
    }
