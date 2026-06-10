from app.mcp.tools.retrieval_tools import (
    retrieve_city_candidates,
    retrieve_stadium_candidates,
    retrieve_route_candidates
)


def run_tests():
    print("--- STARTING MCP RETRIEVAL TOOLS TESTS ---")

    # 1. Test retrieve_city_candidates
    print("\nTesting retrieve_city_candidates for 'midwest'...")
    res = retrieve_city_candidates("midwest")
    print(f"City retrieval result: {res}")
    assert res["success"] is True
    assert len(res["data"]) > 0
    first = res["data"][0]
    assert first["candidate_source"] == "semantic_city"
    assert "city" in first
    assert "retrieval_score" in first
    print("City candidates retrieval test passed!")

    # 2. Test retrieve_stadium_candidates
    print("\nTesting retrieve_stadium_candidates for 'Arrowhead'...")
    res = retrieve_stadium_candidates("Arrowhead")
    print(f"Stadium retrieval result: {res}")
    assert res["success"] is True
    assert len(res["data"]) > 0
    first = res["data"][0]
    assert first["candidate_source"] == "semantic_stadium"
    assert "stadium" in first
    assert "city" in first
    print("Stadium candidates retrieval test passed!")

    # 3. Test retrieve_route_candidates
    print("\nTesting retrieve_route_candidates...")
    res = retrieve_route_candidates(size=2)
    print(f"Route candidates result: {res}")
    assert res["success"] is True
    assert len(res["data"]) > 0
    first = res["data"][0]
    assert first["candidate_source"] == "route"
    assert "city" in first
    assert "match" in first
    print("Route candidates retrieval test passed!")

    print("--- ALL MCP RETRIEVAL TOOLS TESTS PASSED ---")


if __name__ == "__main__":
    run_tests()
