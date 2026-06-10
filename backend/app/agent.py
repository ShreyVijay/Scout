from google.adk.agents import Agent
from app.tools.match_tools import get_team_matches
from app.tools.planner_tools import generate_trip
from app.tools.pivot_tools import check_team_status

root_agent = Agent(
    name="scout",
    model="gemini-2.5-flash",

    description="Adaptive Tournament Intelligence Agent",

    instruction="""
    You help football fans follow teams
    through the World Cup.

    ALWAYS use get_team_matches when a user
    asks for matches of a team.

    Never invent match information.
    """,

    tools=[
        get_team_matches,
        generate_trip,
        check_team_status
    ]
)