from contracts.tournament import TournamentResponse
from app.services.mission_store import get_latest_mission
from app.services.team_status import get_team_status as _get_team_status


def get_team_status(team: str) -> TournamentResponse:
    return TournamentResponse(team=team, status=_get_team_status(team))


def get_tournament_state(team: str) -> TournamentResponse:
    mission = get_latest_mission(team)
    return TournamentResponse(
        team=team,
        status=_get_team_status(team),
        tournament_state=mission.get("tournament_state") if mission else None,
        mission_state=mission.get("mission_state") if mission else None,
    )
