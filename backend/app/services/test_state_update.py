from app.services.state_update_service import (
    update_tournament_state
)

mission = update_tournament_state(
    "Egypt",
    "round_of_16"
)

print(
    mission["tournament_state"]
)

print(
    mission["state_history"]
)