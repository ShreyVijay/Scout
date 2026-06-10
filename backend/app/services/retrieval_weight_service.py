SOURCE_MULTIPLIERS = {
    "route": 1.30,
    "semantic_city": 1.10,
    "semantic_stadium": 1.05
}


def get_source_multiplier(source):
    return SOURCE_MULTIPLIERS.get(
        source,
        1.00
    )