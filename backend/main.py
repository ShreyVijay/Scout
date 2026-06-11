import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.api.travel_routes import router as travel_router
from app.api.google_routes import router as google_router
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.saved_missions import router as saved_missions_router

app = FastAPI(title="skaut")

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

deployed_origins = {
    "https://scout-frontend-436757595175.us-central1.run.app",
    "https://skaut-frontend-436757595175.us-central1.run.app",
}
if "*" not in cors_origins:
    cors_origins = sorted(set(cors_origins).union(deployed_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials="*" not in cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(travel_router)
app.include_router(google_router)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(saved_missions_router)

try:
    from scout_mcp.server import mcp
    app.mount("/mcp", mcp.sse_app())
except ImportError:
    pass

@app.get("/")
def root():
    return {"message": "skaut Backend Running"}

@app.get("/readiness")
def readiness():
    required_variables = [
        "ELASTIC_CLOUD_ID",
        "ELASTIC_USERNAME",
        "ELASTIC_PASSWORD",
        "MONGODB_URI",
        "GOOGLE_MAPS_API_KEY"
    ]
    missing_variables = [name for name in required_variables if not os.getenv(name)]

    if missing_variables:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {
                    "environment": {
                        "status": "failed",
                        "missing": missing_variables,
                    },
                    "elasticsearch": {"status": "skipped"},
                },
            },
        )

    try:
        from app.mcp.elastic_client import get_elastic_client

        if not get_elastic_client().ping():
            raise RuntimeError("Elasticsearch ping failed")
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {
                    "environment": {"status": "ok"},
                    "elasticsearch": {
                        "status": "failed",
                        "error": str(exc),
                    },
                },
            },
        )

    return {"status": "ready"}
