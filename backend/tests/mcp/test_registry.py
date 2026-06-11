import unittest
from scout_mcp.registry import EXPECTED_TOOLS, register_tools, registry

class MockMCPServer:
    def tool(self, name):
        def decorator(func):
            return func
        return decorator

class RegistryTests(unittest.TestCase):
    def test_registry_has_expected_tools(self):
        self.assertEqual(set(registry.keys()), EXPECTED_TOOLS)

    def test_register_tools_succeeds_with_expected_tools(self):
        server = MockMCPServer()
        register_tools(server)

    def test_register_tools_fails_if_mismatch(self):
        server = MockMCPServer()
        # Temporarily modify registry to simulate missing tool
        original_registry = registry.copy()
        try:
            registry.pop("get_mission")
            with self.assertRaises(RuntimeError):
                register_tools(server)
        finally:
            registry.clear()
            registry.update(original_registry)
