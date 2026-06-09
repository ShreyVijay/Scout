from fastapi import FastAPI

app = FastAPI(title="Scout")

@app.get("/")
def root():
    return {"message": "Scout Backend Running"}