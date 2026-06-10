from app.services.search_service import search_matches

def build_trip(team):

    matches = search_matches(team)

    itinerary = []

    for match in matches:

        itinerary.append({
            "city": match["city"],
            "stadium": match["stadium"],
            "date": match["date"]
        })

    return itinerary