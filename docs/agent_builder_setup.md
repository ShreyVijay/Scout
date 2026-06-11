# Elastic Agent Builder Setup

Agent Builder orchestrates Scout; it must not reproduce Scout business logic.

## Register Scout MCP

1. Deploy the standalone Scout MCP server in a network location reachable by Elastic Agent Builder.
2. Configure required Elastic credentials and `MCP_TOOL_TIMEOUT_SECONDS`.
3. Confirm FastAPI `GET /health/mcp` lists all 12 tools.
4. In Elastic Agent Builder, create an MCP connection to the deployed Scout MCP endpoint.
5. Register only the tools listed in `docs/tool_catalog.md`.
6. Keep recommendation, budget, scoring, ranking, and tournament decisions inside Scout services.

## Showcase Workflows

### Recommendation

`get_team_status` -> `get_recommendation` -> `get_reasoning` -> agent response

### Budget

`get_budget` -> `get_recommendation` -> agent response

### City Intelligence

`search_cities` -> `get_city` -> agent response

## Production Rules

- Agent Builder may select/order tools, maintain workflow memory, and expose MCP.
- Do not permit write tools in the initial integration.
- Do not store authentication, user sessions, or raw chat history in `agent_memory`.
- Validate the exact Agent Builder MCP transport and authentication settings against the Elastic deployment version before production activation.
