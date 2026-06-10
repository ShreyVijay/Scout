from app.mcp.server import list_tools, tool_count, fallback_registry


def run_tests():
    print("--- STARTING MCP SERVER HEALTH CHECK TESTS ---")

    # 1. Test tool_count()
    count = tool_count()
    print(f"Tool count: {count}")
    assert count == 9, f"Expected 9 registered tools, got {count}"
    print("Tool count test passed!")

    # 2. Test list_tools()
    tools_data = list_tools()
    assert "tools" in tools_data
    tools_list = tools_data["tools"]
    assert len(tools_list) == 9

    tool_names = [t["name"] for t in tools_list]
    print(f"Registered tools: {tool_names}")

    expected_tools = {
        "get_latest_mission",
        "search_cities",
        "search_stadiums",
        "get_budget_status",
        "get_preferences",
        "retrieve_city_candidates",
        "retrieve_stadium_candidates",
        "retrieve_route_candidates",
        "get_replanning_recommendation"
    }

    for tool_name in expected_tools:
        assert (
            tool_name in tool_names
        ), f"Expected tool {tool_name} to be in registry"
    print("List tools test passed!")

    # 3. Test get_replanning_recommendation exists in registry
    assert "get_replanning_recommendation" in fallback_registry
    print("get_replanning_recommendation existence check passed!")

    print("--- ALL MCP SERVER HEALTH CHECK TESTS PASSED ---")


if __name__ == "__main__":
    run_tests()
