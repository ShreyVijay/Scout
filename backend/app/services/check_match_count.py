from app.services.search_service import search_matches

matches = search_matches("Egypt")

print(len(matches))

for m in matches:
    print(m)