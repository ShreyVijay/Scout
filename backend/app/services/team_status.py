# app/services/team_status.py

TEAM_STATUS = {
    "Egypt": "group_stage"
}

TEAM_STATES = [
    "group_stage",
    "round_of_16",
    "quarter_final",
    "semi_final",
    "final",
    "eliminated"
]

def get_team_status(team: str):
    return TEAM_STATUS.get(team, "unknown")

def set_team_status(team: str, status: str):
    TEAM_STATUS[team] = status