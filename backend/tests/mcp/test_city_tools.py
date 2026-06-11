import unittest
from unittest.mock import patch

from contracts.city import CityResponse
from scout_mcp.tools.city_tools import get_city, search_cities
from tests.mcp.helpers import assert_tool_response


class CityToolTests(unittest.TestCase):
    @patch("scout_mcp.tools.city_tools.city_service.search_cities")
    def test_search_cities(self, service):
        service.return_value = [CityResponse(city="Miami", country="USA")]
        response = search_cities("Miami", 3)
        assert_tool_response(self, response, "search_cities")
        self.assertEqual(response["data"][0]["city"], "Miami")
        service.assert_called_once_with("Miami", 3)

    @patch("scout_mcp.tools.city_tools.city_service.get_city", side_effect=RuntimeError("offline"))
    def test_get_city_structures_errors(self, service):
        response = get_city("Miami")
        assert_tool_response(self, response, "get_city")
        self.assertFalse(response["success"])
        self.assertEqual(response["error"]["type"], "RuntimeError")
