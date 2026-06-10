MISSION_AUTOMATION = {
    ("eliminated", "active"): "monitoring",
    ("eliminated", "monitoring"): "replanning",
    ("quarter_final", "active"): "monitoring",
    ("semi_final", "active"): "monitoring",
    ("eliminated", "planned"): "cancelled",
}

def resolve_mission_state(
    tournament_state,
    mission_state
):
    return MISSION_AUTOMATION.get(
        (tournament_state, mission_state),
        mission_state
    )