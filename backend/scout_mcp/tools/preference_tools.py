from app.services import mission_preference_service, mission_service
from contracts.preference import PreferenceResponse
from scout_mcp.registry import tool


@tool()
def get_preferences(team: str):
    """
    Description:
    Get custom preferences and weights for a team's latest mission.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "preference_id": "...",
        "mission_id": "...",
        "team": "...",
        "travel_style": "...",
        "atmosphere_weight": 0.0,
        "budget_weight": 0.0,
        "transport_weight": 0.0,
        "preference_version": "..."
      },
      "metadata": {
        "tool": "get_preferences",
        "timestamp": "...",
        "version": "v1"
      }
    }

    Example Calls:
    Input:
    {
      "team": "Egypt"
    }
    """
    mission = mission_service.get_mission(team)
    if not mission:
        return None
    
    pref = mission_preference_service.resolve_mission_preferences(mission.mission_id)
    return PreferenceResponse(**pref) if pref else None
