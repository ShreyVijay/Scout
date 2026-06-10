from app.services.city_search import get_city

def calculate_estimated_cost(mission):
    """
    Calculate estimated cost of the mission itinerary by summing city costs.
    """
    if not mission or "itinerary" not in mission or not mission["itinerary"]:
        return {
            "estimated_cost": 0
        }

    total_cost = 0
    for item in mission["itinerary"]:
        city_name = item.get("city")
        if city_name:
            city_data = get_city(city_name)
            if city_data:
                hotel = city_data.get("hotel_cost", 0)
                transport = city_data.get("transport_cost", 0)
                food = city_data.get("food_cost", 0)
                total_cost += (hotel + transport + food)

    return {
        "estimated_cost": total_cost
    }
