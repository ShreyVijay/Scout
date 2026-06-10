from app.services.city_search import get_city
from app.services.stadium_search import get_city_stadiums

def get_city_intelligence(city_name):
    """
    Aggregate city and stadium information for the given city.
    """
    city_info = get_city(city_name)
    if not city_info:
        return None

    # Retrieve associated stadiums
    stadiums = get_city_stadiums(city_name)

    # Construct the unified intelligence object
    return {
        "city": city_info.get("city"),
        "country": city_info.get("country"),
        "atmosphere_score": city_info.get("atmosphere_score"),
        "budget_score": city_info.get("budget_score"),
        "transport_score": city_info.get("transport_score"),
        "fan_zone_score": city_info.get("fan_zone_score"),
        "description": city_info.get("description"),
        "stadiums": stadiums
    }
