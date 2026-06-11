import unittest
from unittest.mock import patch

from contracts.stadium import StadiumResponse
from scout_mcp.tools.stadium_tools import get_stadium, search_stadiums
from tests.mcp.helpers import assert_tool_response


class StadiumToolTests(unittest.TestCase):
    @patch("scout_mcp.tools.stadium_tools.stadium_service.search_stadiums")
    def test_search_stadiums_only_invokes_service(self, service):
        service.return_value = [StadiumResponse(stadium="SoFi Stadium", city="Los Angeles")]
        response = search_stadiums("SoFi", 2)
        assert_tool_response(self, response, "search_stadiums")
        self.assertTrue(response["success"])
        self.assertEqual(response["data"][0]["stadium"], "SoFi Stadium")
        service.assert_called_once_with("SoFi", 2)

    @patch("scout_mcp.tools.stadium_tools.stadium_service.get_stadium", return_value=None)
    def test_get_stadium_not_found_is_deterministic(self, service):
        response = get_stadium("Missing")
        assert_tool_response(self, response, "get_stadium")
        self.assertTrue(response["success"])
        self.assertIsNone(response["data"])
