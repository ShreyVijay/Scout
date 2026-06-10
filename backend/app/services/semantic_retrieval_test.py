# backend/app/services/semantic_retrieval_test.py

from app.services.semantic_candidate_service import (
    retrieve_city_candidates,
    retrieve_stadium_candidates
)


def run_tests():

    print(
        "--- STARTING SEMANTIC RETRIEVAL TESTS ---"
    )

    # ==========================================
    # Test 1: "coastal football city"
    # Expected: Miami or Los Angeles returned
    # ==========================================

    print("\n=== Test 1: coastal football city ===")

    results = retrieve_city_candidates(
        "coastal football city"
    )

    print(f"Results count: {len(results)}")

    for r in results:
        print(
            f"  City: {r['city']}, "
            f"Score: {r['retrieval_score']:.4f}, "
            f"Tags: {r.get('tags', [])}"
        )

    city_names = [
        r["city"] for r in results
    ]

    assert len(results) > 0, (
        "Expected at least 1 result "
        "for 'coastal football city'"
    )

    assert (
        "Miami" in city_names
        or "Los Angeles" in city_names
    ), (
        f"Expected Miami or Los Angeles "
        f"in results, got {city_names}"
    )

    print("Test 1 passed!")

    # ==========================================
    # Test 2: "midwest atmosphere"
    # Expected: Kansas City returned
    # ==========================================

    print("\n=== Test 2: midwest atmosphere ===")

    results = retrieve_city_candidates(
        "midwest atmosphere"
    )

    print(f"Results count: {len(results)}")

    for r in results:
        print(
            f"  City: {r['city']}, "
            f"Score: {r['retrieval_score']:.4f}, "
            f"Tags: {r.get('tags', [])}"
        )

    city_names = [
        r["city"] for r in results
    ]

    assert len(results) > 0, (
        "Expected at least 1 result "
        "for 'midwest atmosphere'"
    )

    assert "Kansas City" in city_names, (
        f"Expected Kansas City "
        f"in results, got {city_names}"
    )

    print("Test 2 passed!")

    # ==========================================
    # Test 3: "SoFi" (stadium search)
    # Expected: SoFi Stadium returned
    # ==========================================

    print("\n=== Test 3: SoFi ===")

    results = retrieve_stadium_candidates(
        "SoFi"
    )

    print(f"Results count: {len(results)}")

    for r in results:
        print(
            f"  Stadium: {r['stadium']}, "
            f"City: {r['city']}, "
            f"Score: {r['retrieval_score']:.4f}"
        )

    stadium_names = [
        r["stadium"] for r in results
    ]

    assert len(results) > 0, (
        "Expected at least 1 result "
        "for 'SoFi'"
    )

    assert "SoFi Stadium" in stadium_names, (
        f"Expected SoFi Stadium "
        f"in results, got {stadium_names}"
    )

    print("Test 3 passed!")

    # ==========================================
    # Test 4: "tropical" (city search)
    # Expected: Miami returned (description match)
    # ==========================================

    print("\n=== Test 4: tropical ===")

    results = retrieve_city_candidates(
        "tropical"
    )

    print(f"Results count: {len(results)}")

    for r in results:
        print(
            f"  City: {r['city']}, "
            f"Score: {r['retrieval_score']:.4f}"
        )

    city_names = [
        r["city"] for r in results
    ]

    assert "Miami" in city_names, (
        f"Expected Miami "
        f"in results, got {city_names}"
    )

    print("Test 4 passed!")

    # ==========================================
    # Test 5: "Arrowhead" (stadium search)
    # Expected: GEHA Field at Arrowhead Stadium
    # ==========================================

    print("\n=== Test 5: Arrowhead ===")

    results = retrieve_stadium_candidates(
        "Arrowhead"
    )

    print(f"Results count: {len(results)}")

    for r in results:
        print(
            f"  Stadium: {r['stadium']}, "
            f"City: {r['city']}, "
            f"Score: {r['retrieval_score']:.4f}"
        )

    assert len(results) > 0, (
        "Expected at least 1 result "
        "for 'Arrowhead'"
    )

    found_arrowhead = any(
        "Arrowhead" in r["stadium"]
        for r in results
    )

    assert found_arrowhead, (
        f"Expected Arrowhead stadium "
        f"in results"
    )

    print("Test 5 passed!")

    # ==========================================
    # Test 6: Verify retrieval_score is present
    # and positive for all results
    # ==========================================

    print("\n=== Test 6: Retrieval score validation ===")

    results = retrieve_city_candidates(
        "stadium city"
    )

    for r in results:

        assert "retrieval_score" in r, (
            "Missing retrieval_score field"
        )

        assert r["retrieval_score"] > 0, (
            f"Expected positive retrieval_score, "
            f"got {r['retrieval_score']}"
        )

    print("Test 6 passed!")

    print(
        "\n--- ALL SEMANTIC RETRIEVAL "
        "TESTS PASSED SUCCESSFULLY ---"
    )


if __name__ == "__main__":
    run_tests()
