REPLANNING_STATES = [
    "quarter_final",
    "semi_final",
    "final",
    "eliminated"
]

def needs_replanning(
    old_state,
    new_state
):

    if new_state == "eliminated":
        return True

    if old_state != new_state and new_state in REPLANNING_STATES:
        return True

    return False