from datetime import datetime

def build_transition(
    state_type,
    old_state,
    new_state
):

    return {
        "state_type": state_type,
        "from": old_state,
        "to": new_state,
        "timestamp": datetime.utcnow().isoformat()
    }