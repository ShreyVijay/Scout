# Scout MCP Architecture

## Boundary

Elastic Cloud remains the source of truth. Scout services own business logic and datastore access. The standalone `backend/mcp/` package owns tool exposure, response envelopes, timeouts, logging, and metrics.

```text
Elastic Agent Builder
        |
        v
FastMCP server / tool registry
        |
        v
MCP read-only tools
        |
        v
Typed Scout service facades
        |
        v
Existing Scout services -> Elastic Cloud
```

MCP tools never query Elasticsearch and never implement recommendation, budget, scoring, ranking, or tournament logic.

## Contracts

Stable Pydantic DTOs live in `backend/contracts/`. Existing variable Elastic documents permit extra fields for compatibility, but every required public field is validated.

Every tool returns:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "metadata": {
    "tool": "get_recommendation",
    "timestamp": "2026-06-11T00:00:00+00:00",
    "latency_ms": 12.4
  }
}
```

## Runtime

Start from `backend/`:

```bash
python -m mcp.server
```

`MCP_TOOL_TIMEOUT_SECONDS` defaults to `30`. FastAPI exposes registry status and metrics at `GET /health/mcp`.
