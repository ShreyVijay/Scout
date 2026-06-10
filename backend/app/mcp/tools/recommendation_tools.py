from app.mcp.schemas import error_response, success_response
from app.services.mission_store import get_latest_mission
from app.services.replanning_engine import run_replanning


def get_replanning_recommendation(mission=None, team: str | None = None):
    try:
        resolved_mission = mission

        if isinstance(mission, str) and team is None:
            team = mission
            resolved_mission = None

        if resolved_mission is None and team:
            resolved_mission = get_latest_mission(team)

        if not resolved_mission:
            return success_response(None)

        result = run_replanning(resolved_mission)
        return success_response(result)
    except Exception as exc:
        return error_response(exc)
