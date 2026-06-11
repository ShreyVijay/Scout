from contracts.base import ScoutDTO


class TournamentResponse(ScoutDTO):
    team: str
    status: str
    tournament_state: str | None = None
    mission_state: str | None = None
