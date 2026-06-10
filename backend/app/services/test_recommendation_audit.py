from app.services.recommendation_audit_service import (
    build_recommendation_audit
)


def run_tests():

    print(
        "--- STARTING AUDIT TESTS ---"
    )

    rankings = [
        {
            "city": "Miami",
            "rank": 1,
            "final_score": 10.14,
            "candidate_source": "route",
            "contributions": {
                "atmosphere": 5.0,
                "budget": 1.2,
                "transport": 1.6
            }
        },
        {
            "city": "Los Angeles",
            "rank": 2,
            "final_score": 9.49,
            "candidate_source": "route",
            "contributions": {
                "atmosphere": 4.0,
                "budget": 1.5,
                "transport": 1.8
            }
        },
        {
            "city": "Kansas City",
            "rank": 3,
            "final_score": 9.23,
            "candidate_source": "route",
            "contributions": {
                "atmosphere": 3.0,
                "budget": 2.7,
                "transport": 1.4
            }
        }
    ]

    result = (
        build_recommendation_audit(
            rankings
        )
    )

    assert (
        "audit"
        in result
    )

    assert (
        len(
            result["audit"]
        ) == 3
    )

    assert (
        result["winner"]
        == "Miami"
    )

    assert (
        result["audit"][0]["city"]
        == "Miami"
    )

    print(
        "Audit structure passed"
    )

    print(
        "--- ALL AUDIT TESTS PASSED ---"
    )


if __name__ == "__main__":
    run_tests()