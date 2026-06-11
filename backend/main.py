import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.api.travel_routes import router as travel_router
from app.api.google_routes import router as google_router

app = FastAPI(title="Scout")

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

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

try:
    from scout_mcp.server import mcp
    app.mount("/mcp", mcp.sse_app())
except ImportError:
    pass

@app.get("/")
def root():
    return {"message": "Scout Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readiness")
def readiness():
    required_variables = [
        "ELASTIC_CLOUD_ID",
        "ELASTIC_USERNAME",
        "ELASTIC_PASSWORD",
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


@app.get("/health/mcp")
def mcp_health():
    from scout_mcp.metrics import get_tool_metrics
    from scout_mcp.registry import list_tools
    from scout_mcp.tools import (
        budget_tools,
        city_tools,
        mission_tools,
        preference_tools,
        recommendation_tools,
        stadium_tools,
        tournament_tools,
    )

    return {
        "healthy": True,
        "tool_count": len(list_tools()),
        "tools": list_tools(),
        "metrics": get_tool_metrics(),
        "version": "v1",
        "sdk": "FastMCP"
    }
