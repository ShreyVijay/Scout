from app.services.candidate_enrichment_service import (
    enrich_candidates
)

from app.services.candidate_scoring_service import (
    score_candidates
)


def choose_candidate(
    candidates,
    preferences,
    remaining_budget
):
    if not candidates:
        return {
            "winner": None,
            "rankings": []
        }

    enriched = enrich_candidates(
        candidates
    )

    scored = score_candidates(
        enriched,
        preferences,
        remaining_budget
    )

    rankings = sorted(
        scored,
        key=lambda x: (
            -x.get(
                "final_score",
                0.0
            ),
            x.get(
                "city",
                ""
            )
        )
    )

    for i, candidate in enumerate(
        rankings,
        start=1
    ):
        candidate["rank"] = i

    winner = rankings[0]

    return {
        "winner": winner,
        "rankings": rankings
    }