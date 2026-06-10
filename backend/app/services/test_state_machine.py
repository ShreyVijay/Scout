from app.services.state_service import validate_transition
from app.core.state_machine import (
    TOURNAMENT_TRANSITIONS,
    MISSION_TRANSITIONS
)

print("Tournament Tests")
print(
    validate_transition(
        "group_stage",
        "round_of_16",
        TOURNAMENT_TRANSITIONS
    )
)

print(
    validate_transition(
        "group_stage",
        "final",
        TOURNAMENT_TRANSITIONS
    )
)

print()

print("Mission Tests")

print(
    validate_transition(
        "created",
        "planned",
        MISSION_TRANSITIONS
    )
)

print(
    validate_transition(
        "created",
        "completed",
        MISSION_TRANSITIONS
    )
)