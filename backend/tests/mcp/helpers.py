def assert_tool_response(testcase, response, tool_name):
    testcase.assertEqual(response["metadata"]["tool"], tool_name)
    testcase.assertIn("timestamp", response["metadata"])
    testcase.assertIn("latency_ms", response["metadata"])
    testcase.assertEqual(response["metadata"]["version"], "v1")
    testcase.assertIn("success", response)
    if response.get("success"):
        testcase.assertIn("data", response)
        testcase.assertNotIn("error", response)
    else:
        testcase.assertIn("error", response)
        testcase.assertNotIn("data", response)

