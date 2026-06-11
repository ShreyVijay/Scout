import unittest
from unittest.mock import patch

from contracts.mission import MissionResponse
from scout_mcp.tools.preference_tools import get_preferences
from tests.mcp.helpers import assert_tool_response

MISSION = MissionResponse(
    mission_id="m-1",
    team="Egypt",
    budget={"total_budget": 3000},
    travel_style="Comfort",
    objective="Support Egypt",
    mission_state="planned",
    tournament_state="group_stage",
)

class PreferenceToolTests(unittest.TestCase):
    @patch("scout_mcp.tools.preference_tools.mission_service.get_mission", return_value=MISSION)
    @patch("scout_mcp.tools.preference_tools.mission_preference_service.resolve_mission_preferences")
    def test_get_preferences(self, resolve, get_mission):
        resolve.return_value = {
            "preference_id": "p-1",
            "mission_id": "m-1",
            "team": "Egypt",
            "travel_style": "Comfort",
            "atmosphere_weight": 0.5,
            "budget_weight": 0.5,
            "transport_weight": 0.5,
            "preference_version": "v1"
        }
        response = get_preferences("Egypt")
        assert_tool_response(self, response, "get_preferences")
        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["atmosphere_weight"], 0.5)
        resolve.assert_called_once_with("m-1")
