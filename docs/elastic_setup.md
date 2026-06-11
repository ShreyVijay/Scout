# Elastic Setup for Scout MCP

## Existing Source-of-Truth Indices

Scout currently uses indices including `missions`, `cities`, `stadiums`, `team_progress`, preferences, events, and alternative routes. MCP accesses them only through Scout services.

## Agent Memory Index

Create the approved summary-only memory index:

```bash
cd backend
python -m app.services.create_agent_memory_index
```

Mapping:

```json
{
  "memory_type": "keyword",
  "mission_id": "keyword",
  "summary": "text",
  "timestamp": "date"
}
```

Allowed `memory_type` values:

- `mission_summary`
- `recommendation_summary`
- `reasoning_summary`

Never store chat history, user sessions, authentication data, secrets, or tokens.

## Access Control

Use a dedicated least-privilege Elastic service account. Grant read access to Scout source indices and read/write/create-index access only to `agent_memory`. Configure snapshots, lifecycle policy, and alerting before enabling production memory writes.
