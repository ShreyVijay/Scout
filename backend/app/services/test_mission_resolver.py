from app.services.mission_state_resolver import (
    resolve_mission_state
)

print(
    resolve_mission_state(
        "eliminated",
        "monitoring"
    )
)

print(
    resolve_mission_state(
        "quarter_final",
        "active"
    )
)