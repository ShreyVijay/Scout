from app.services.stadium_search import get_stadium, get_city_stadiums, get_all_stadiums

def test_stadium_search_all():
    print("--- Testing Stadium Search Service ---")

    # 1. Test exact lookup
    print("Testing exact lookup for MetLife Stadium...")
    metlife = get_stadium("MetLife Stadium")
    assert metlife is not None
    assert metlife["stadium"] == "MetLife Stadium"
    assert metlife["city"] == "New York"
    print("Exact lookup passed.")

    # 2. Test city filter
    print("Testing city filtering for Dallas...")
    dallas_stadiums = get_city_stadiums("Dallas")
    assert len(dallas_stadiums) == 1
    assert dallas_stadiums[0]["stadium"] == "AT&T Stadium"
    print("City filtering passed.")

    # 3. Test get all
    print("Testing retrieve all...")
    all_stadiums = get_all_stadiums()
    assert len(all_stadiums) == 8
    print("Retrieve all passed.")
    print("Stadium Search Tests Passed Successfully!\n")

if __name__ == "__main__":
    test_stadium_search_all()
