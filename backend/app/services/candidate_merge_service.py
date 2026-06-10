ALLOWED_CANDIDATE_SOURCES = {
    "route",
    "semantic_city",
    "semantic_stadium"
}


def _retrieval_score(candidate):
    score = candidate.get("retrieval_score")
    if score is None:
        return 0.0
    return float(score)


def _normalize_route_candidate(candidate):
    city = candidate.get("city")
    if not city:
        return None

    normalized = candidate.copy()
    normalized.update({
        "city": city,
        "match": candidate.get("match"),
        "reason": candidate.get("reason", ""),
        "candidate_source": "route"
    })

    return normalized


def _normalize_semantic_city_candidate(candidate):
    city = candidate.get("city")
    if not city:
        return None

    normalized = candidate.copy()
    normalized.update({
        "city": city,
        "match": candidate.get("match"),
        "reason": candidate.get("description", ""),
        "candidate_source": "semantic_city"
    })

    return normalized


def _normalize_semantic_stadium_candidate(candidate):
    city = candidate.get("city")
    if not city:
        return None

    stadium = candidate.get("stadium")
    description = candidate.get("description", "")
    reason = description
    if stadium:
        reason = f"{stadium}: {description}" if description else stadium

    normalized = candidate.copy()
    normalized.update({
        "city": city,
        "match": candidate.get("match"),
        "reason": reason,
        "candidate_source": "semantic_stadium"
    })

    return normalized


def _merge_candidate(merged_by_city, candidate):
    if candidate is None:
        return

    source = candidate.get("candidate_source")
    if source not in ALLOWED_CANDIDATE_SOURCES:
        return

    city_key = candidate["city"].lower()
    existing = merged_by_city.get(city_key)

    if (
        existing is None
        or _retrieval_score(candidate) > _retrieval_score(existing)
    ):
        merged_by_city[city_key] = candidate


def merge_candidates(
    route_candidates,
    semantic_city_candidates,
    semantic_stadium_candidates
):
    """
    Normalizes and deduplicates candidate sources into raw replanning
    candidates. This does not score, rank, enrich, or filter candidates.
    """
    merged_by_city = {}

    for candidate in route_candidates:
        _merge_candidate(
            merged_by_city,
            _normalize_route_candidate(candidate)
        )

    for candidate in semantic_city_candidates:
        _merge_candidate(
            merged_by_city,
            _normalize_semantic_city_candidate(candidate)
        )

    for candidate in semantic_stadium_candidates:
        _merge_candidate(
            merged_by_city,
            _normalize_semantic_stadium_candidate(candidate)
        )

    return list(merged_by_city.values())
