# Scout MCP Tool Catalog

| Tool | Service boundary | Output |
|---|---|---|
| `get_mission(team)` | `mission_service` | Latest mission DTO |
| `get_mission_history(team, size)` | `mission_service` | Mission DTO list |
| `search_cities(query, size)` | `city_service` | City DTO list |
| `get_city(city)` | `city_service` | City DTO or null |
| `search_stadiums(query, size)` | `stadium_service` | Stadium DTO list |
| `get_stadium(stadium)` | `stadium_service` | Stadium DTO or null |
| `get_budget(team)` | `budget_service` | Budget DTO or null |
| `get_team_status(team)` | `tournament_service` | Tournament DTO |
| `get_tournament_state(team)` | `tournament_service` | Tournament DTO |
| `get_recommendation(team)` | `recommendation_service` | Recommendation DTO or null |
| `get_reasoning(team)` | `reasoning_service` | Reasoning DTO or null |
| `get_audit(team)` | `audit_service` | Audit DTO or null |

All tools are read-only. Null data is a successful not-found result; service/runtime failures return `success: false` with a structured error.
