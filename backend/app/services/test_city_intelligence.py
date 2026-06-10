from app.services.city_intelligence import get_city_intelligence

def test_city_intelligence_all():
    print("--- Testing City Intelligence Engine ---")

    # 1. Verify aggregation payload
    print("Testing aggregation for Los Angeles...")
    la_intel = get_city_intelligence("Los Angeles")
    assert la_intel is not None
    assert la_intel["city"] == "Los Angeles"
    assert la_intel["atmosphere_score"] == 92
    assert len(la_intel["stadiums"]) == 1
    assert la_intel["stadiums"][0]["stadium"] == "SoFi Stadium"
    print("Aggregation payload correctness verified.")

    # 2. Verify aggregation for missing city
    print("Testing missing city intelligence aggregation...")
    missing_intel = get_city_intelligence("Gotham")
    assert missing_intel is None
    print("Missing city aggregation verified.")
    print("City Intelligence Engine Tests Passed Successfully!\n")

if __name__ == "__main__":
    test_city_intelligence_all()
