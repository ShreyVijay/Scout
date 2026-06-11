from pydantic import Field

from contracts.base import ScoutDTO


class CityResponse(ScoutDTO):
    city: str
    country: str | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
