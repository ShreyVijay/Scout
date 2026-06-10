from app.services.mission_preference_service import resolve_mission_preferences
from app.services.fan_preference_service import (
    get_preferences_by_mission,
    update_preferences as update_preferences_db,
    create_preferences as create_preferences_db
)

def get_preferences(mission_id: str):
    """
    Retrieves the fan preferences (weights for atmosphere, budget, and transport) for a mission.
    If no preferences are explicitly set, resolves and returns the default fallback preference configuration.
    """
    try:
        pref = resolve_mission_preferences(mission_id)
        cleaned = {k: v for k, v in pref.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}
        return cleaned
    except Exception as e:
        return f"Error retrieving preferences: {str(e)}"

def update_preferences(
    mission_id: str,
    atmosphere_weight: float,
    budget_weight: float,
    transport_weight: float
):
    """
    Updates or initializes the fan preference weights (atmosphere, budget, transport) for a mission.
    All weights must be floats. The engine will normalize the weights so they sum exactly to 1.0.
    """
    try:
        pref = resolve_mission_preferences(mission_id)
        pref["atmosphere_weight"] = float(atmosphere_weight)
        pref["budget_weight"] = float(budget_weight)
        pref["transport_weight"] = float(transport_weight)

        existing = get_preferences_by_mission(mission_id)
        if existing:
            pref["_elastic_id"] = existing["_elastic_id"]
            pref["_seq_no"] = existing["_seq_no"]
            pref["_primary_term"] = existing["_primary_term"]
            res = update_preferences_db(pref)
        else:
            res = create_preferences_db(pref)

        cleaned = {k: v for k, v in res.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}
        return cleaned
    except Exception as e:
        return f"Error updating preferences: {str(e)}"
