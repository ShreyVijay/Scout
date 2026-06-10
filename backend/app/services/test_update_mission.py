from app.services.mission_store import (
    get_latest_mission,
    update_mission
)

mission = get_latest_mission("Egypt")

mission["tournament_state"] = "round_of_16"

update_mission(mission)

print("updated")