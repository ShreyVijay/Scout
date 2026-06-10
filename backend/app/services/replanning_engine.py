from app.services.replanning_candidate_service import (
    get_candidates
)

from app.services.replanning_decision_service import (
    choose_candidate
)

from app.services.replanning_reasoning_service import (
    generate_reasoning
)

from app.services.mission_preference_service import (
    resolve_mission_preferences
)

from app.services.recommendation_audit_service import (
    build_recommendation_audit
)


def run_replanning(
    mission
):
    mission_id = mission.get(
        "mission_id"
    )

    preferences = (
        resolve_mission_preferences(
            mission_id
        )
    )

    if (
        "budget_intelligence"
        not in mission
    ):
        from app.services.mission_budget_service import (
            integrate_mission_budget
        )

        mission = (
            integrate_mission_budget(
                mission,
                spent_budget=0
            )
        )

    remaining_budget = (
        mission[
            "budget_intelligence"
        ][
            "projected_remaining_budget"
        ]
    )

    candidates = (
        get_candidates(
            mission
        )
    )

    decision_result = (
        choose_candidate(
            candidates,
            preferences,
            remaining_budget
        )
    )

    winner = decision_result.get(
        "winner"
    )

    rankings = decision_result.get(
        "rankings",
        []
    )

    reasoning = (
        generate_reasoning(
            winner,
            preferences
        )
    )

    audit = (
        build_recommendation_audit(
            rankings
        )
    )

    return {
        "recommendation": winner,
        "rankings": rankings,
        "reasoning": reasoning,
        "audit": audit
    }