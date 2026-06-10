from app.services.mission_state_service import (
    update_mission_state
)

mission = update_mission_state(
    "Egypt",
    "active"
)

print(
    mission["mission_state"]
)

print(
    mission["state_history"]
)