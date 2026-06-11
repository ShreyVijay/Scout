from contracts.stadium import StadiumResponse
from app.services.stadium_search import get_stadium as _get_stadium
from app.services.stadium_search import search_stadiums as _search_stadiums


def get_stadium(stadium: str) -> StadiumResponse | None:
    result = _get_stadium(stadium)
    return StadiumResponse.model_validate(result) if result else None


def search_stadiums(query: str, size: int = 10) -> list[StadiumResponse]:
    return [StadiumResponse.model_validate(item) for item in _search_stadiums(query, size)]
