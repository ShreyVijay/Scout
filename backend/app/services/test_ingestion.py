from app.services.data_ingestion import ingest_matches

count = ingest_matches(
    "../datasets/egypt_matches.json"
)

print(count)