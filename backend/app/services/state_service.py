from app.core.state_machine import (
    TOURNAMENT_TRANSITIONS,
    MISSION_TRANSITIONS
)

def validate_transition(
    current_state,
    next_state,
    transition_map
):

    return (
        next_state in
        transition_map.get(current_state, [])
    )