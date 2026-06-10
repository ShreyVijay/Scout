from planner import build_trip

trip = build_trip("Egypt")

for stop in trip:
    print(stop)