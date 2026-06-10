TOURNAMENT_TRANSITIONS = {
    "group_stage": ["round_of_16", "eliminated"],
    "round_of_16": ["quarter_final", "eliminated"],
    "quarter_final": ["semi_final", "eliminated"],
    "semi_final": ["final", "eliminated"],
    "final": ["champion", "eliminated"],
    "champion": [],
    "eliminated": []
}

MISSION_TRANSITIONS = {
    "created": ["planned"],
    "planned": ["active", "cancelled"],
    "active": ["monitoring", "completed", "cancelled"],
    "monitoring": ["replanning", "completed", "cancelled"],
    "replanning": ["active"],
    "completed": [],
    "cancelled": []
}