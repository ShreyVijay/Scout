import unittest
from unittest.mock import patch

from contracts.tournament import TournamentResponse
from scout_mcp.tools.tournament_tools import get_team_status, get_tournament_state
from tests.mcp.helpers import assert_tool_response


class TournamentToolTests(unittest.TestCase):
    @patch("scout_mcp.tools.tournament_tools.tournament_service.get_team_status")
    def test_get_team_status(self, service):
        service.return_value = TournamentResponse(team="Egypt", status="group_stage")
        response = get_team_status("Egypt")
        assert_tool_response(self, response, "get_team_status")
        self.assertEqual(response["data"]["status"], "group_stage")

    @patch("scout_mcp.tools.tournament_tools.tournament_service.get_tournament_state")
    def test_get_tournament_state(self, service):
        service.return_value = TournamentResponse(
            team="Egypt",
            status="group_stage",
            tournament_state="group_stage",
            mission_state="active",
        )
        response = get_tournament_state("Egypt")
        assert_tool_response(self, response, "get_tournament_state")
        self.assertEqual(response["data"]["mission_state"], "active")
