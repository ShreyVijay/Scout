from app.mcp.schemas import error_response, success_response
from app.services.mission_store import get_latest_mission as service_get_latest_mission


def get_latest_mission(team: str):
    try:
        mission = service_get_latest_mission(team)
        return success_response(mission)
    except Exception as exc:
        return error_response(exc)
