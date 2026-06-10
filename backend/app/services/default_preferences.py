# backend/app/services/default_preferences.py

def get_default_preferences():
    """
    Generates default weight mapping for fan preferences.
    """
    return {
        "atmosphere_weight": 0.5,
        "budget_weight": 0.3,
        "transport_weight": 0.2,
        "preference_version": 1
    }
