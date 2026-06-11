from app.mcp.schemas import error_response, success_response
from app.services.stadium_search import get_city_stadiums as service_get_city_stadiums
from app.services.stadium_service import get_stadium as service_get_stadium
from app.services.stadium_service import search_stadiums as service_search_stadiums


def get_stadium(stadium: str):
    try:
        result = service_get_stadium(stadium)
        return success_response(result.model_dump(mode="json") if result else None)
    except Exception as exc:
        return error_response(exc)


def get_city_stadiums(city: str):
    try:
        return success_response(service_get_city_stadiums(city))
    except Exception as exc:
        return error_response(exc)


def search_stadiums(query: str, size: int = 10):
    try:
        stadiums = service_search_stadiums(query, size)
        return success_response([item.model_dump(mode="json") for item in stadiums])
    except Exception as exc:
        return error_response(exc)
