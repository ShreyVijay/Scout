# Scout MCP Implementation Review

This document performs a detailed verification pass over the Scout MCP read-only layer implementation.

## Summary of the MCP Architecture

The MCP layer sits cleanly on top of the existing Scout services:
```text
MCP Client
    ↓ (MCP Protocol)
MCP Server (mcp/server.py)
    ↓ (Tool dispatch)
MCP Wrapper (mcp/tools/*)
    ↓ (Import & invoke)
Existing Scout Service (services/*, tools/*)
    ↓
Elasticsearch
```

---

## Detailed File-by-File Review

### 1. [elastic_client.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/elastic_client.py)
* **Purpose**: Provides a lazily initialized, shared Elasticsearch client instance for MCP tools to prevent duplicate clients.
* **Wrapped services**: Built-in Elasticsearch module.
* **Dependencies**: `elasticsearch`, `python-dotenv`.
* **Potential bugs**: If `.env` credentials are changed dynamically in-memory, the client caching will not reflect this without a server restart.
* **Missing imports**: None.
* **Contract mismatches**: None.
* **Unused code**: None.
* **Test coverage**: Verified by integration tests querying Elasticsearch.

### 2. [schemas.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/schemas.py)
* **Purpose**: Defines standardized schema dataclasses (`ToolResponse`, etc.) and helper response formatting functions (`success_response`, `error_response`) to ensure a unified format for all MCP tools.
* **Wrapped services**: None.
* **Dependencies**: Standard library `dataclasses`, `typing`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: None.
* **Unused code**: Dataclasses like `MissionResponse`, `CityResponse`, `StadiumResponse`, `BudgetResponse`, `PreferenceResponse`, and `RecommendationResponse` are defined but not directly instantiated in the tool wrappers, which return formatted dictionaries using `success_response` and `error_response`. This is acceptable for clean documentation/type hints.
* **Test coverage**: None.

### 3. [mission_tools.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/tools/mission_tools.py)
* **Purpose**: Wraps the mission retrieval service to expose team missions to the MCP layer.
* **Wrapped services**: `get_latest_mission`.
* **Dependencies**: `app.services.mission_store`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: Returns `success_response(mission)`. If no mission exists, `get_latest_mission` returns `None`, which is wrapped inside a successful response.
* **Unused code**: None.
* **Test coverage**: Tested in integration tests.

### 4. [city_tools.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/tools/city_tools.py)
* **Purpose**: Exposes search and lookup capabilities for cities to the MCP layer.
* **Wrapped services**: `get_city`, `get_all_cities`, `search_city`.
* **Dependencies**: `app.services.city_search`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: List slicing (`results[:size]`) is safe.
* **Unused code**: `get_all_cities` is implemented but is not required to be registered in the MCP server.
* **Test coverage**: Covered by city tools tests.

### 5. [stadium_tools.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/tools/stadium_tools.py)
* **Purpose**: Exposes stadium query functions and implements a custom fuzzy multi-match `search_stadiums` against Elasticsearch.
* **Wrapped services**: `get_stadium`, `get_city_stadiums`.
* **Dependencies**: `app.mcp.elastic_client`, `app.services.stadium_search`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: `search_stadiums` correctly uses the shared MCP client.
* **Unused code**: `get_stadium` and `get_city_stadiums` are wrapped but not registered on the server (which only exposes `search_stadiums`).
* **Test coverage**: Verified by integration tests.

### 6. [budget_tools.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/tools/budget_tools.py)
* **Purpose**: Exposes trip estimation and budget status tools.
* **Wrapped services**: `get_budget_status`, `estimate_trip_cost`.
* **Dependencies**: `app.tools.budget_tools`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: None.
* **Unused code**: `estimate_trip_cost` is wrapped but not in the required server tool list.
* **Test coverage**: Verified by end-to-end tests.

### 7. [preference_tools.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/tools/preference_tools.py)
* **Purpose**: Retrieves resolved fan preference configurations.
* **Wrapped services**: `get_preferences`.
* **Dependencies**: `app.tools.preference_tools`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: None.
* **Unused code**: None.
* **Test coverage**: Covered in end-to-end preference tests.

### 8. [retrieval_tools.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/tools/retrieval_tools.py)
* **Purpose**: Performs candidate retrieval from semantic search indices or alternative routes.
* **Wrapped services**: `retrieve_city_candidates`, `retrieve_stadium_candidates`, `get_alternative_routes`.
* **Dependencies**: `app.services.alternative_search`, `app.services.semantic_candidate_service`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: Enriches retrieval responses with `candidate_source` metadata.
* **Unused code**: None.
* **Test coverage**: Verified by `test_mcp_retrieval.py`.

### 9. [recommendation_tools.py](file:///c:/Users/BIT/Desktop/Scout/backend/app/mcp/tools/recommendation_tools.py)
* **Purpose**: Triggers adaptive replanning for a given team or mission.
* **Wrapped services**: `run_replanning`.
* **Dependencies**: `app.services.mission_store`, `app.services.replanning_engine`.
* **Potential bugs**: None.
* **Missing imports**: None.
* **Contract mismatches**: Handles argument polymorphism gracefully (checks if a mission object is passed or if a string represents a team name to retrieve the latest mission).
* **Unused code**: None.
* **Test coverage**: Verified by `test_mcp_recommendation.py`.
