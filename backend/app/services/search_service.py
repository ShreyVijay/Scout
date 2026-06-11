"""
Dynamic tournament match generator for the FIFA World Cup 2026 hackathon demo.

Instead of relying on Elasticsearch data that may be incomplete,
this module generates a realistic 3-match Group Stage itinerary
for any of the 48 qualified teams, using real host cities, stadiums,
and tournament dates.
"""

import hashlib
from datetime import datetime, timedelta

# All 16 host cities with their stadiums
HOST_VENUES = [
    {"city": "Mexico City", "stadium": "Estadio Azteca"},
    {"city": "Guadalajara", "stadium": "Estadio Akron"},
    {"city": "Monterrey", "stadium": "Estadio BBVA"},
    {"city": "Los Angeles", "stadium": "SoFi Stadium"},
    {"city": "San Francisco", "stadium": "Levi's Stadium"},
    {"city": "Seattle", "stadium": "Lumen Field"},
    {"city": "Kansas City", "stadium": "Arrowhead Stadium"},
    {"city": "Dallas", "stadium": "AT&T Stadium"},
    {"city": "Houston", "stadium": "NRG Stadium"},
    {"city": "Atlanta", "stadium": "Mercedes-Benz Stadium"},
    {"city": "Miami", "stadium": "Hard Rock Stadium"},
    {"city": "Philadelphia", "stadium": "Lincoln Financial Field"},
    {"city": "New York/New Jersey", "stadium": "MetLife Stadium"},
    {"city": "Boston", "stadium": "Gillette Stadium"},
    {"city": "Toronto", "stadium": "BMO Field"},
    {"city": "Vancouver", "stadium": "BC Place"},
]

# 48 qualified teams mapped to groups A-L
GROUPS = {
    "A": ["Mexico", "TBD-A2", "TBD-A3", "TBD-A4"],
    "B": ["Canada", "TBD-B2", "TBD-B3", "TBD-B4"],
    "C": ["USA", "TBD-C2", "TBD-C3", "TBD-C4"],
    "D": ["Argentina", "TBD-D2", "TBD-D3", "TBD-D4"],
    "E": ["Brazil", "France", "TBD-E3", "TBD-E4"],
    "F": ["England", "Germany", "TBD-F3", "TBD-F4"],
    "G": ["Spain", "Netherlands", "TBD-G3", "TBD-G4"],
    "H": ["Portugal", "Uruguay", "TBD-H3", "TBD-H4"],
    "I": ["Japan", "South Korea", "Morocco", "TBD-I4"],
    "J": ["Belgium", "Croatia", "Colombia", "TBD-J4"],
    "K": ["Egypt", "Senegal", "Australia", "TBD-K4"],
    "L": ["Switzerland", "Austria", "Norway", "TBD-L4"],
}

# Reverse lookup: team -> group
TEAM_GROUP = {}
for group, teams in GROUPS.items():
    for t in teams:
        TEAM_GROUP[t] = group

# All 48 qualified team names (for validation and auto-assignment)
ALL_TEAMS = [
    "Canada", "Mexico", "USA",
    "Australia", "Iraq", "Iran", "Japan", "Jordan", "South Korea",
    "Qatar", "Saudi Arabia", "Uzbekistan",
    "Algeria", "Cape Verde", "DR Congo", "Ivory Coast", "Egypt",
    "Ghana", "Morocco", "Senegal", "South Africa", "Tunisia",
    "Curacao", "Haiti", "Panama",
    "Argentina", "Brazil", "Colombia", "Ecuador", "Paraguay", "Uruguay",
    "New Zealand",
    "Austria", "Belgium", "Bosnia and Herzegovina", "Croatia", "Czechia",
    "England", "France", "Germany", "Netherlands", "Norway", "Portugal",
    "Scotland", "Spain", "Sweden", "Switzerland", "Türkiye",
]

GROUP_STAGE_START = datetime(2026, 6, 11)


def _team_hash(team: str) -> int:
    """Deterministic hash so the same team always gets the same venues."""
    return int(hashlib.md5(team.encode()).hexdigest(), 16)


def search_matches(team: str) -> list[dict]:
    """
    Generate a realistic 3-match Group Stage itinerary for the given team.
    Each match is assigned a different host city/stadium and a date
    spread across the group stage window (Jun 11 – Jun 25).
    """
    h = _team_hash(team)

    # Pick 3 distinct venues deterministically
    indices = []
    for i in range(3):
        idx = (h + i * 7) % len(HOST_VENUES)
        while idx in indices:
            idx = (idx + 1) % len(HOST_VENUES)
        indices.append(idx)

    venues = [HOST_VENUES[i] for i in indices]

    # Spread matches across the group stage: day 0, day 5, day 10
    matches = []
    for i, venue in enumerate(venues):
        match_date = GROUP_STAGE_START + timedelta(days=i * 5)
        matches.append({
            "city": venue["city"],
            "stadium": venue["stadium"],
            "date": match_date.strftime("%Y-%m-%d"),
            "team": team,
            "stage": "Group Stage",
            "match_number": i + 1,
        })

    return matches