from app.mcp.schemas import error_response, success_response
from app.tools.preference_tools import get_preferences as service_get_preferences


def get_preferences(mission_id: str):
    try:
        return success_response(service_get_preferences(mission_id))
    except Exception as exc:
        return error_response(exc)
