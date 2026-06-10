from app.services.city_intelligence import get_city_intelligence
from app.services.stadium_search import get_city_stadiums as search_city_stadiums

def get_city_info(city: str):
    """
    Returns unified intelligence about a city, including scores and stadiums.
    """
    return get_city_intelligence(city)

def get_city_stadiums(city: str):
    """
    Returns all stadiums located in a given city.
    """
    return search_city_stadiums(city)
