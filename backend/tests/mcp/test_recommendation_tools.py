import unittest
from unittest.mock import patch

from contracts.recommendation import AuditResponse, ReasoningResponse, RecommendationResponse
from scout_mcp.schemas.base import ProvenanceMetadata
from scout_mcp.tools.recommendation_tools import get_audit, get_reasoning, get_recommendation
from tests.mcp.helpers import assert_tool_response


class RecommendationToolTests(unittest.TestCase):
    @patch("scout_mcp.tools.recommendation_tools.recommendation_service.get_recommendation")
    def test_get_recommendation(self, service):
        service.return_value = RecommendationResponse(
            city="Miami", 
            rank=1,
            provenance=ProvenanceMetadata(candidate_source="semantic", retrieval_score=0.99)
        )
        response = get_recommendation("Egypt")
        assert_tool_response(self, response, "get_recommendation")
        self.assertEqual(response["data"]["city"], "Miami")
        self.assertEqual(response["data"]["provenance"]["candidate_source"], "semantic")
        service.assert_called_once_with("Egypt")

    @patch("scout_mcp.tools.recommendation_tools.reasoning_service.get_reasoning")
    def test_get_reasoning(self, service):
        service.return_value = ReasoningResponse(decision="Miami", reasons=["Highest score"])
        response = get_reasoning("Egypt")
        assert_tool_response(self, response, "get_reasoning")
        self.assertTrue(response["success"])

    @patch("scout_mcp.tools.recommendation_tools.audit_service.get_audit")
    def test_get_audit(self, service):
        service.return_value = AuditResponse(winner="Miami")
        response = get_audit("Egypt")
        assert_tool_response(self, response, "get_audit")
        self.assertEqual(response["data"]["winner"], "Miami")
