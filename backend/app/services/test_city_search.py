from app.services.city_search import get_city, search_city, search_by_tag, get_all_cities

def test_city_search_all():
    print("--- Testing City Search Service ---")

    # 1. Test exact lookup
    print("Testing exact lookup for New York...")
    nyc = get_city("New York")
    assert nyc is not None
    assert nyc["city"] == "New York"
    assert nyc["country"] == "USA"
    print("Exact lookup passed.")

    # 2. Test missing lookup
    print("Testing missing lookup...")
    missing = get_city("Atlantis")
    assert missing is None
    print("Missing lookup passed.")

    # 3. Test tag lookup
    print("Testing tag lookup for 'Coastal'...")
    coastal_cities = search_by_tag("Coastal")
    assert len(coastal_cities) > 0
    # Make sure at least NY and LA and Boston are returned since they have 'Coastal' tag
    coastal_names = [c["city"] for c in coastal_cities]
    print(f"Coastal cities found: {coastal_names}")
    assert "New York" in coastal_names
    assert "Los Angeles" in coastal_names
    print("Tag lookup passed.")

    # 4. Test fuzzy search on description/name
    print("Testing fuzzy search for 'metropolis'...")
    metropolis_matches = search_city("metropolis")
    assert len(metropolis_matches) > 0
    names = [c["city"] for c in metropolis_matches]
    print(f"Metropolis search matches: {names}")
    assert "New York" in names or "Los Angeles" in names
    print("Fuzzy search passed.")

    # 5. Test retrieve all
    print("Testing retrieve all...")
    all_cities = get_all_cities()
    assert len(all_cities) == 8
    print("Retrieve all passed.")
    print("City Search Tests Passed Successfully!\n")

if __name__ == "__main__":
    test_city_search_all()
