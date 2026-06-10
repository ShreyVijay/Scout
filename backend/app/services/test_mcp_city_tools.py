from app.mcp.tools.city_tools import search_cities
from app.mcp.tools.stadium_tools import search_stadiums


def run_tests():
    print("--- STARTING MCP CITY AND STADIUM TOOLS TESTS ---")

    # 1. Test search_cities
    print("\nTesting search_cities for 'Miami'...")
    res = search_cities("Miami")
    print(f"City search result: {res}")
    assert res["success"] is True
    assert len(res["data"]) > 0
    assert any(c["city"] == "Miami" for c in res["data"])
    print("City search test passed!")

    # 2. Test search_stadiums
    print("\nTesting search_stadiums for 'SoFi'...")
    res = search_stadiums("SoFi")
    print(f"Stadium search result: {res}")
    assert res["success"] is True
    assert len(res["data"]) > 0
    assert any("SoFi" in s["stadium"] for s in res["data"])
    print("Stadium search test passed!")

    print("--- ALL MCP CITY AND STADIUM TOOLS TESTS PASSED ---")


if __name__ == "__main__":
    run_tests()
