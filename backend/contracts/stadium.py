from contracts.base import ScoutDTO


class StadiumResponse(ScoutDTO):
    stadium: str
    city: str | None = None
    country: str | None = None
    capacity: int | None = None
    description: str | None = None
