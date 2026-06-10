import re

def parse_mission(text: str):

    team = None
    budget = None
    travel_style = "Balanced"

    teams = [
        "Egypt",
        "Brazil",
        "Argentina",
        "France",
        "England",
        "Germany",
        "Spain",
        "Portugal"
    ]

    for t in teams:
        if t.lower() in text.lower():
            team = t
            break

    budget_match = re.search(r"\$?(\d+)", text)

    if budget_match:
        budget = int(budget_match.group(1))

    text_lower = text.lower()

    if "atmosphere" in text_lower:
        travel_style = "Atmosphere"

    elif "budget" in text_lower:
        travel_style = "Budget"

    elif "football" in text_lower:
        travel_style = "Purist"

    objective = text.strip()

    return {
        "team": team,
        "budget": budget,
        "travel_style": travel_style,
        "objective": objective
    }