from google.adk.agents import Agent

from app.tools.match_tools import (
    get_team_matches,
    generate_trip
)

root_agent = Agent(
    name="scout",

    model="gemini-2.5-flash",

    description="""
    Adaptive Tournament Intelligence Agent
    """,

    instruction="""
    You help football fans follow teams
    through the World Cup.

    Use tools whenever team data
    or itinerary generation is needed.

    Never invent match information.
    Always retrieve it.
    """,

    tools=[
        get_team_matches,
        generate_trip
    ]
)