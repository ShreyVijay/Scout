from app.services.mission_store import (
    get_latest_mission,
    update_mission
)

from app.services.state_transition_service import (
    build_transition
)

def save_transition(
    mission,
    state_type,
    old_state,
    new_state
):

    transition = build_transition(
        state_type,
        old_state,
        new_state
    )

    mission["state_history"].append(
        transition
    )