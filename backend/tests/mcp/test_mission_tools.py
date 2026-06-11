import unittest
from unittest.mock import patch

from contracts.mission import MissionResponse
from scout_mcp.tools.mission_tools import get_mission, get_mission_history
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


class MissionToolTests(unittest.TestCase):
    @patch("scout_mcp.tools.mission_tools.mission_service.get_mission", return_value=MISSION)
    def test_get_mission_invokes_service_and_validates_shape(self, service):
        response = get_mission("Egypt")
        assert_tool_response(self, response, "get_mission")
        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["mission_id"], "m-1")
        service.assert_called_once_with("Egypt")

    @patch("scout_mcp.tools.mission_tools.mission_service.get_history", return_value=[MISSION])
    def test_get_mission_history_invokes_service(self, service):
        response = get_mission_history("Egypt", 5)
        assert_tool_response(self, response, "get_mission_history")
        self.assertTrue(response["success"])
        self.assertEqual(len(response["data"]), 1)
        service.assert_called_once_with("Egypt", size=5)
