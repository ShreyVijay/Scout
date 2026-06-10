from app.services.state_transition_service import build_transition

transition = build_transition(
    "tournament",
    "group_stage",
    "round_of_16"
)

print(transition)