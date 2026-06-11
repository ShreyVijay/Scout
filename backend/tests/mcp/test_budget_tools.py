import unittest
from unittest.mock import patch

from contracts.budget import BudgetResponse
from scout_mcp.tools.budget_tools import get_budget
from tests.mcp.helpers import assert_tool_response


class BudgetToolTests(unittest.TestCase):
    @patch("scout_mcp.tools.budget_tools.budget_service.get_budget")
    def test_get_budget(self, service):
        service.return_value = BudgetResponse(
            total_budget=3000,
            spent_budget=500,
            estimated_cost=1000,
            projected_remaining_budget=1500,
            risk_level="LOW",
        )
        response = get_budget("Egypt")
        assert_tool_response(self, response, "get_budget")
        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["risk_level"], "LOW")
        service.assert_called_once_with("Egypt")
