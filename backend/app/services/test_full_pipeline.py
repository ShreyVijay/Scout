from app.services.event_store import save_event
from app.services.tournament_evaluator import (
    process_latest_event
)
from app.services.mission_store import (
    get_latest_mission
)

mission = get_latest_mission(
    "Egypt"
)

print("CURRENT STATE:")
print(mission["tournament_state"])

save_event(
    "Egypt",
    "advanced",
    mission["tournament_state"],
    "champion"
)

mission = process_latest_event(
    "Egypt"
)

print()
print("RESULT:")
print(mission)