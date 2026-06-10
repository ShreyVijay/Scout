from app.services.state_service import (
    validate_transition
)

from app.services.state_transition_service import (
    build_transition
)

from app.core.state_machine import (
    MISSION_TRANSITIONS
)

def update_mission_state(
    mission,
    new_state
):

    current_state = mission["mission_state"]

    if not validate_transition(
        current_state,
        new_state,
        MISSION_TRANSITIONS
    ):
        raise Exception(
            f"Invalid transition: {current_state} -> {new_state}"
        )

    transition = build_transition(
        "mission",
        current_state,
        new_state
    )

    mission["mission_state"] = new_state

    mission["state_history"].append(
        transition
    )

    return mission