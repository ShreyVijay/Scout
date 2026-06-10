from app.services.city_search import get_city

def enrich_candidate(candidate):
    """
    Enriches a single raw candidate by fetching its city metadata and calculating candidate_cost.
    Preserves candidate metadata by copying the original candidate and appending enrichment fields.
    """
    city_name = candidate.get("city")
    city_info = get_city(city_name)
    if not city_info:
        city_info = {}

    hotel_cost = city_info.get("hotel_cost", 0)
    transport_cost = city_info.get("transport_cost", 0)
    food_cost = city_info.get("food_cost", 0)
    candidate_cost = hotel_cost + transport_cost + food_cost

    enriched = candidate.copy()
    enriched.update({
        "city": city_name,
        "match": candidate.get("match"),
        "reason": candidate.get("reason"),
        "country": city_info.get("country"),
        "description": city_info.get("description"),
        "hotel_cost": hotel_cost,
        "transport_cost": transport_cost,
        "food_cost": food_cost,
        "candidate_cost": candidate_cost,
        "atmosphere_score": city_info.get("atmosphere_score", 0.0),
        "budget_score": city_info.get("budget_score", 0.0),
        "transport_score": city_info.get("transport_score", 0.0),
        "fan_zone_score": city_info.get("fan_zone_score", 0.0)
    })
    return enriched

def enrich_candidates(candidates):
    """
    Enriches a list of raw candidates.
    """
    return [enrich_candidate(c) for c in candidates]
