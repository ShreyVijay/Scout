from app.mcp.schemas import error_response, success_response
from app.services.city_search import (
    get_city as service_get_city,
    get_all_cities as service_get_all_cities,
    search_city as service_search_city
)


def get_city(city: str):
    try:
        return success_response(service_get_city(city))
    except Exception as exc:
        return error_response(exc)


def search_cities(query: str, size: int = 10):
    try:
        results = service_search_city(query)
        return success_response(results[:size])
    except Exception as exc:
        return error_response(exc)


def get_all_cities(size: int = 100):
    try:
        results = service_get_all_cities()
        return success_response(results[:size])
    except Exception as exc:
        return error_response(exc)
