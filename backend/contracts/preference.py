from contracts.base import ScoutDTO


class PreferenceResponse(ScoutDTO):
    preference_id: str | None = None
    mission_id: str | None = None
    team: str | None = None
    travel_style: str | None = None
    atmosphere_weight: float | None = None
    budget_weight: float | None = None
    transport_weight: float | None = None
    preference_version: str | None = None
