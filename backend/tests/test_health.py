import os
import unittest
from unittest.mock import patch

from fastapi.responses import JSONResponse

from app.api.health import health
from main import readiness


class HealthEndpointTests(unittest.TestCase):
    def test_health_is_ok(self):
        self.assertEqual(health(), {"status": "ok"})

    def test_mcp_health_is_ok(self):
        from app.api.health import mcp_health
        response = mcp_health()

        self.assertTrue(response["healthy"])
        self.assertEqual(response["tool_count"], 13)
        self.assertEqual(response["version"], "v1")
        self.assertEqual(response["sdk"], "FastMCP")

    def test_readiness_reports_missing_required_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            response = readiness()

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 503)

    @patch("app.mcp.elastic_client.get_elastic_client")
    def test_readiness_is_ready_when_elasticsearch_is_available(self, get_client):
        get_client.return_value.ping.return_value = True
        environment = {
            "ELASTIC_CLOUD_ID": "test-cloud",
            "ELASTIC_USERNAME": "test-user",
            "ELASTIC_PASSWORD": "test-password",
            "MONGODB_URI": "mongodb://localhost:27017/scout",
            "GOOGLE_MAPS_API_KEY": "test-key"
        }

        with patch.dict(os.environ, environment, clear=True):
            self.assertEqual(readiness(), {"status": "ready"})



if __name__ == "__main__":
    unittest.main()
