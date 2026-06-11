from contracts.city import CityResponse
from app.services.city_search import get_city as _get_city
from app.services.city_search import search_city as _search_city


def get_city(city: str) -> CityResponse | None:
    result = _get_city(city)
    return CityResponse.model_validate(result) if result else None


def search_cities(query: str, size: int = 10) -> list[CityResponse]:
    return [CityResponse.model_validate(item) for item in _search_city(query)[:size]]
