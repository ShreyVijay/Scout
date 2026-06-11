from typing import Any

from pydantic import Field

from contracts.base import ScoutDTO


class MissionResponse(ScoutDTO):
    mission_id: str
    team: str
    budget: dict[str, Any] | float | int
    travel_style: str
    objective: str
    itinerary: list[dict[str, Any]] = Field(default_factory=list)
    mission_state: str
    tournament_state: str
    state_history: list[dict[str, Any]] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None
