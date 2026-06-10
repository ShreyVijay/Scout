# app/services/test_team_status.py

from app.services.team_status_store import (
    save_team_status,
    get_latest_team_status
)

save_team_status(
    "Egypt",
    "quarter_final"
)

print(
    get_latest_team_status("Egypt")
)