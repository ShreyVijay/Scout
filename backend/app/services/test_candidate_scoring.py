from app.services.candidate_scoring_service import (
    score_candidate
)


def run_tests():

    print(
        "--- STARTING CANDIDATE SCORING UNIT TESTS ---"
    )

    candidate = {
        "city": "Miami",
        "atmosphere_score": 10.0,
        "budget_score": 4.0,
        "transport_score": 8.0,
        "fan_zone_score": 10.0,
        "candidate_cost": 220.0
    }

    preferences = {
        "atmosphere_weight": 0.5,
        "budget_weight": 0.3,
        "transport_weight": 0.2
    }

    # Scenario 1
    res = score_candidate(
        candidate,
        preferences,
        remaining_budget=300.0
    )

    assert abs(
        res["raw_score"] - 7.8
    ) < 1e-9, (
        f"Expected raw_score 7.8, got {res['raw_score']}"
    )

    assert abs(
        res["final_score"] - 7.8
    ) < 1e-9, (
        f"Expected final_score 7.8, got {res['final_score']}"
    )

    assert abs(
        res["contributions"]["atmosphere"] - 5.0
    ) < 1e-9

    assert abs(
        res["contributions"]["budget"] - 1.2
    ) < 1e-9

    assert abs(
        res["contributions"]["transport"] - 1.6
    ) < 1e-9

    print(
        "Scenario 1: No penalty score test passed."
    )

    # Scenario 2
    res = score_candidate(
        candidate,
        preferences,
        remaining_budget=110.0
    )

    assert abs(
        res["raw_score"] - 7.8
    ) < 1e-9

    assert abs(
        res["final_score"] - 3.9
    ) < 1e-9, (
        f"Expected final_score 3.9, got {res['final_score']}"
    )

    print(
        "Scenario 2: Proportional penalty score test passed."
    )

    # Scenario 3
    res = score_candidate(
        candidate,
        preferences,
        remaining_budget=-50.0
    )

    expected_score = (
        7.8 / 220.0
    )

    assert abs(
        res["final_score"] - expected_score
    ) < 1e-9, (
        f"Expected final_score {expected_score}, got {res['final_score']}"
    )

    print(
        "Scenario 3: Zero/Negative remaining budget penalty score test passed."
    )

    print(
        "--- ALL CANDIDATE SCORING UNIT TESTS PASSED SUCCESSFULLY ---"
    )


if __name__ == "__main__":
    run_tests()