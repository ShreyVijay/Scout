# Scout V1.5 Elastic MCP Readiness Report

Generated: 2026-06-10
Scope: Audit only. No MCP implementation, production code changes, test changes, refactors, Maps work, or probability modeling.

## Section 1 - Current Architecture Diagram

Current V1.5 architecture:

```text
User / Agent
    |
    v
Mission Creation and Mission Store
    |
    v
Tournament Intelligence
    |
    v
Replanning Trigger
    |
    v
Candidate Retrieval
    |-- alternative_routes
    |-- semantic city retrieval
    |-- semantic stadium retrieval
    |
    v
Candidate Merge
    |
    v
Candidate Enrichment
    |
    v
Candidate Scoring
    |
    v
Decision Engine
    |
    v
Reasoning Engine
    |
    v
Recommendation
```

Current Elastic usage pattern:

```text
Service module
    |
    | creates module-level Elasticsearch client from .env
    v
Elasticsearch Cloud index
    |
    v
Raw dict response returned to caller
```

Proposed MCP boundary:

```text
Agent / Client
    |
    v
Scout MCP Server
    |
    |-- mission tools
    |-- tournament tools
    |-- retrieval tools
    |-- city/stadium tools
    |-- budget/preference tools
    |-- recommendation tools
    |
    v
Scout service layer
    |
    v
Elasticsearch Cloud
```

## Section 2 - Repository Audit Findings

Files reviewed:

- `backend/app/agent.py`
- `backend/app/agents/scout_agent.py`
- `backend/app/tools/match_tools.py`
- `backend/app/tools/planner_tools.py`
- `backend/app/tools/pivot_tools.py`
- `backend/app/tools/budget_tools.py`
- `backend/app/tools/city_tools.py`
- `backend/app/tools/preference_tools.py`
- `backend/app/services/search_service.py`
- `backend/app/services/city_search.py`
- `backend/app/services/stadium_search.py`
- `backend/app/services/semantic_candidate_service.py`
- `backend/app/services/alternative_search.py`
- `backend/app/services/candidate_merge_service.py`
- `backend/app/services/candidate_enrichment_service.py`
- `backend/app/services/candidate_scoring_service.py`
- `backend/app/services/replanning_candidate_service.py`
- `backend/app/services/replanning_decision_service.py`
- `backend/app/services/replanning_reasoning_service.py`
- `backend/app/services/replanning_engine.py`
- `backend/app/services/mission_service.py`
- `backend/app/services/mission_store.py`
- `backend/app/services/event_store.py`
- `backend/app/services/tournament_evaluator.py`
- `backend/app/services/mission_budget_service.py`
- `backend/app/services/budget_profile_service.py`
- `backend/app/services/fan_preference_service.py`
- `backend/app/services/mission_preference_service.py`
- `backend/app/services/budget_intelligence.py`
- `backend/app/services/budget_calculator.py`
- `backend/app/services/budget_risk_engine.py`
- `backend/app/services/city_intelligence.py`
- `backend/app/services/mission_city_service.py`
- `backend/app/services/create_match_events_index.py`
- `backend/app/services/reset_missions.py`
- `backend/app/services/create_city_index.py`
- `backend/app/services/create_stadium_index.py`
- `backend/app/services/create_budget_profiles_index.py`
- `backend/app/services/create_fan_preferences_index.py`
- `backend/app/services/load_alternatives.py`
- `backend/app/services/load_cities.py`
- `backend/app/services/load_stadiums.py`

High-level findings:

- Scout is partially ready for Elastic MCP. The domain services are modular enough to wrap as MCP tools, and the V1.5 retrieval-to-reasoning path now preserves metadata.
- The main blocker is not domain logic. It is operational hardening: shared Elasticsearch client management, typed contracts, error envelopes, pagination/limits, and citation metadata.
- Search and retrieval services are simple and useful but return raw dictionaries. MCP tools should expose stable schemas rather than direct service internals.
- Agent registration is not yet MCP-ready. There are two agent entry points with different tool lists, and `backend/app/agents/scout_agent.py` imports `generate_trip` from `app.tools.match_tools`, while the actual implementation is in `planner_tools.py`.
- Index creation and load scripts are mixed with destructive reset behavior. MCP integration should not depend on scripts that delete/recreate production indexes.
- Optimistic locking exists for missions and fan preferences, but not consistently for budget profiles or events.
- Retrieval metadata survives the V1.5 recommendation path, but evidence citations are not yet first-class objects.

## Section 3 - Index Audit

### `missions`

Observed schema source: `reset_missions.py`, V1.2/V1.5 pipeline tests.

Fields:

- `mission_id`: keyword
- `team`: keyword
- `budget`: object with budget totals and risk fields
- `travel_style`: keyword
- `objective`: text
- `mission_state`: keyword
- `tournament_state`: keyword
- `requires_replanning`: boolean
- `created_at`: date
- `updated_at`: date
- `itinerary`: nested with `city`, `stadium`, `date`
- `state_history`: nested with `state_type`, `from`, `to`, `timestamp`

Audit:

- Schema quality: Good for MVP state tracking. Nested itinerary and history are appropriate.
- Searchability: Good for exact team/state lookups; weaker for mission text discovery because `objective` lacks explicit analyzers and no `mission_id` lookup helper is centralized beyond preference resolution.
- Retrieval quality: Good for mission state; not designed for semantic retrieval.
- Missing fields: `budget_intelligence` is written into mission objects at runtime but is not explicitly mapped in `reset_missions.py`. Recommendation history, reasoning snapshots, and evidence/citation metadata are also missing.
- MCP compatibility: Medium-high. Mission tools can wrap `get_latest_mission`, `save_mission`, and `update_mission`, but update tools need strict input schemas and concurrency behavior.
- Scaling risks: `get_latest_mission(team)` assumes latest mission by team is the right mission. This will break when multiple users follow the same team or when a user has multiple missions.

### `match_events`

Observed schema source: `create_match_events_index.py`, `event_store.py`.

Fields:

- `team`: keyword
- `event_type`: keyword
- `from_stage`: keyword
- `to_stage`: keyword
- `event_time`: date
- `processed`: boolean

Audit:

- Schema quality: Good for queue MVP.
- Searchability: Good for team + processed + chronological event processing.
- Retrieval quality: Good for deterministic event queue behavior.
- Missing fields: No event source, confidence, payload, external event ID, ingestion timestamp, processed timestamp, error status, retry count, or event provenance.
- MCP compatibility: Medium. Read tools are straightforward, but write tools need guardrails because event insertion changes mission state.
- Scaling risks: Deterministic event ID includes `event_time`, so duplicate protection depends on exact timestamp equality. There is no dead-letter state for repeatedly failing events.

### `cities`

Observed schema source: `create_city_index.py`, `load_cities.py`.

Fields:

- `city`: keyword
- `country`: keyword
- `description`: text
- `tags`: keyword
- cost fields: integer
- score fields: integer
- `created_at`: date

Audit:

- Schema quality: Good for structured city intelligence. Scoring fields are explicit.
- Searchability: Moderate. `description` is searchable; `city` is keyword-only, so wildcard searches are used for partial city lookup.
- Retrieval quality: Good for MVP lexical retrieval. No vector fields, embeddings, synonyms, geospatial fields, or tournament-specific metadata.
- Missing fields: host country/region normalization, geo coordinates, airport codes, venue links, evidence/source URL, source freshness, language, aliases, and canonical city ID.
- MCP compatibility: High for read-only city tools. Medium for semantic retrieval tools until query/output contracts are formalized.
- Scaling risks: Wildcard over keyword fields can become expensive. City document IDs use city names, which may collide globally without country/region.

### `stadiums`

Observed schema source: `create_stadium_index.py`, `load_stadiums.py`.

Fields:

- `stadium`: keyword
- `city`: keyword
- `country`: keyword
- `capacity`: integer
- `description`: text
- `atmosphere_score`: integer
- `transport_score`: integer
- `created_at`: date

Audit:

- Schema quality: Good MVP stadium facts.
- Searchability: Moderate. Description search works; stadium/city wildcard search is used for flexible matching.
- Retrieval quality: Good for simple stadium discovery. No vector fields, aliases, venue IDs, geo coordinates, or schedule joins.
- Missing fields: `tags`, source metadata, aliases, venue coordinates, opening/renovation data, city canonical ID, accessibility/transport evidence.
- MCP compatibility: High for read-only stadium lookup tools.
- Scaling risks: Stadium name as document ID may collide or change. Wildcard queries can degrade at scale.

### `budget_profiles`

Observed schema source: `create_budget_profiles_index.py`, `budget_profile_service.py`.

Fields:

- `profile_id`: keyword
- `mission_id`: keyword
- `team`: keyword
- `total_budget`: integer
- `spent_budget`: integer
- `remaining_budget`: integer
- `risk_level`: keyword
- `created_at`: date
- `updated_at`: date

Audit:

- Schema quality: Solid MVP profile record.
- Searchability: Good for exact IDs and mission/team filtering if helpers are added.
- Retrieval quality: Adequate for budget tools.
- Missing fields: currency, cost model version, budget line items, confidence, source, audit trail, estimated cost, projected remaining budget.
- MCP compatibility: Medium. Reads are easy; writes need optimistic locking and validation.
- Scaling risks: `update_budget_profile` replaces by index without optimistic locking. MCP write tools would need stronger concurrency rules.

### `fan_preferences`

Observed schema source: `create_fan_preferences_index.py`, `fan_preference_service.py`.

Fields:

- `preference_id`: keyword
- `mission_id`: keyword
- `team`: keyword
- `travel_style`: keyword
- `atmosphere_weight`: float
- `budget_weight`: float
- `transport_weight`: float
- `preference_version`: integer
- `created_at`: date
- `updated_at`: date

Audit:

- Schema quality: Good. Version and optimistic locking metadata are handled in service responses.
- Searchability: Good by mission/team/travel style.
- Retrieval quality: Good for current recommendation model.
- Missing fields: user ID, explanation of preference source, preference history, last agent/user update actor.
- MCP compatibility: High for read/update tools if exposed with validation and concurrency semantics.
- Scaling risks: No user scoping. Multiple fans following the same team need separate preference documents.

### `alternative_routes`

Observed schema source: `load_alternatives.py`.

Fields:

- `type`: keyword
- `city`: keyword
- `match`: keyword
- `reason`: text

Audit:

- Schema quality: Minimal but useful.
- Searchability: Low to moderate. Current service uses `match_all`, not a query.
- Retrieval quality: Static fallback candidates only.
- Missing fields: route ID, stage/date, target team, tournament state, source, retrieval score, rank, cost estimate, city canonical ID.
- MCP compatibility: Medium. It can become a read-only fallback tool, but it should not be the main intelligent retrieval tool.
- Scaling risks: Current retrieval is unfiltered and returns all routes. It will become noisy as the index grows.

## Section 4 - Service Audit

### Search services

Reviewed:

- `search_service.py`
- `city_search.py`
- `stadium_search.py`
- `semantic_candidate_service.py`
- `alternative_search.py`

MCP suitability:

- `search_matches(team)` can become `get_team_matches`.
- `get_city(city_name)`, `search_city(query_str)`, `search_by_tag(tag)`, and `get_all_cities()` can become city intelligence tools.
- `get_stadium(stadium_name)`, `get_city_stadiums(city_name)`, and `get_all_stadiums()` can become stadium tools.
- `retrieve_city_candidates(query_text, size)` and `retrieve_stadium_candidates(query_text, size)` can become semantic candidate tools.
- `get_alternative_routes()` can become a fallback route retrieval tool, but should add filters before MCP scale.

Abstraction needs:

- Centralize Elasticsearch client creation. Currently almost every service creates its own module-level client.
- Define typed input/output schemas per tool. Current services return raw dicts.
- Add standard error envelopes. Several services catch broad exceptions and return `None` or strings.
- Add explicit limits and pagination for all list/search tools.
- Add provenance metadata to retrieval results: index, doc ID, score, query, source fields, and citation-ready payload.

Coupling:

- Search services are coupled directly to Elasticsearch index names.
- Replanning candidate generation is coupled to `alternative_routes`, `cities`, and `stadiums`.
- Budget calculation is coupled to city lookup and city cost fields.

Refactoring needed before MCP:

- Required: Shared Elastic access layer or client provider.
- Required: Stable tool contracts with validation.
- Required: Read/write tool separation.
- Recommended: Service result objects that include `data`, `metadata`, and `errors`.

## Section 5 - Agent Audit

Reviewed:

- `backend/app/agent.py`
- `backend/app/agents/scout_agent.py`
- `backend/app/tools/*.py`

Current architecture:

- Google ADK `Agent` is used.
- `backend/app/agent.py` registers `get_team_matches`, `generate_trip`, and `check_team_status`.
- `backend/app/agents/scout_agent.py` registers `get_team_matches` and `generate_trip`, but imports both from `app.tools.match_tools`. In the reviewed code, `generate_trip` lives in `planner_tools.py`, not `match_tools.py`.
- Tool wrappers are thin functions over services.
- Tool output schemas are implicit.

MCP integration strategy:

```text
ADK Agent
    |
    | local tools for orchestration and UX
    v
Scout MCP client adapter
    |
    v
Scout MCP server
    |
    v
Typed service adapters
    |
    v
Elasticsearch-backed Scout services
```

Required changes before MCP:

- Choose one canonical agent entry point.
- Normalize tool imports and registration.
- Add MCP tool contracts rather than exposing raw service functions directly.
- Separate read-only tools from mutating tools.
- Add tool descriptions that define when the agent should call each tool.
- Add response schemas for mission, city, stadium, retrieval candidates, recommendations, and reasoning.

Risks:

- Duplicate agent entry points can cause drift.
- Thin tools return raw dicts or strings, making agent behavior harder to constrain.
- MCP write tools could mutate mission or preference state without concurrency/permission guardrails unless scoped carefully.

## Section 6 - MCP Readiness Score

| Area | Score | Rationale |
|:---|---:|:---|
| Retrieval | 78 | Semantic and route candidate retrieval exist, merge is implemented, and metadata survives. Needs provenance, citations, and better query normalization. |
| Data Quality | 64 | Core MVP data is mapped and loaded, but source metadata, canonical IDs, user IDs, geo fields, aliases, and freshness are missing. |
| Search | 70 | Elasticsearch search is functional and tested. Wildcard usage, raw dict contracts, and lack of shared error handling reduce readiness. |
| Agent Layer | 48 | ADK tools exist, but duplicate agent definitions, inconsistent tool registration, and implicit schemas make direct MCP integration risky. |
| Explainability | 67 | Reasoning includes candidate source, retrieval score, score metadata, reasons, and contributions. Needs evidence citations and source documents. |
| Scalability | 52 | MVP indexes are small and simple. Scaling risks include wildcard queries, unfiltered route retrieval, module-level clients, no pagination in several services, and weak multi-user modeling. |

Overall readiness: 63 / 100.

Interpretation: Scout is ready for an MCP design spike and read-only MCP prototype, but not ready for production MCP exposure until P0 hardening is complete.

## Section 7 - Required Changes Before MCP

### P0 - Required before MCP prototype

1. Establish a single Elasticsearch client/provider module.
   - Evidence: Most service files instantiate their own `Elasticsearch(...)` client.
   - Impact: Reduces duplicated config, improves testing, and gives MCP one place for credentials/timeouts/retries.

2. Define MCP-safe schemas for tool inputs and outputs.
   - Evidence: Services return raw dicts and sometimes strings/`None`.
   - Impact: Prevents agent confusion and makes tool behavior predictable.

3. Canonicalize agent entry point and tool registration.
   - Evidence: `agent.py` and `agents/scout_agent.py` diverge; `scout_agent.py` imports `generate_trip` from the wrong module based on reviewed files.
   - Impact: MCP registration needs one source of truth.

4. Add provenance fields to retrieval outputs.
   - Evidence: Retrieval returns `retrieval_score` but not `_id`, index, query, matched fields, or citation text.
   - Impact: Required for citation flow and explainability.

5. Separate read-only MCP tools from mutating MCP tools.
   - Evidence: Tools can update preferences, trigger replanning, and eventually mutate mission state.
   - Impact: Prevents accidental state changes from agent exploration.

### P1 - Required before production MCP

1. Add pagination and hard limits to all list/search tools.
2. Replace wildcard-heavy searches with safer query patterns or `search_as_you_type`/edge n-gram fields where needed.
3. Add user/session scoping to missions, preferences, and recommendations.
4. Add structured error handling and observability around every Elastic call.
5. Add recommendation history index or mission-attached recommendation snapshots.
6. Add citation/evidence objects into reasoning output.
7. Add optimistic locking to budget profile writes.

### P2 - Useful after MCP baseline

1. Add vector/semantic fields for cities, stadiums, and route alternatives.
2. Add aliases and canonical IDs for city/stadium entities.
3. Add geospatial fields for future Maps integration.
4. Add source freshness and trust metadata for city/stadium/budget data.
5. Add tool-level audit logs for MCP calls.

## Section 8 - Elastic MCP Architecture Proposal

### Proposed service layout

```text
backend/app/mcp/
    server.py
    schemas.py
    elastic_client.py
    tools/
        mission_tools.py
        tournament_tools.py
        retrieval_tools.py
        city_tools.py
        stadium_tools.py
        budget_tools.py
        preference_tools.py
        recommendation_tools.py
```

### Proposed MCP tool layout

Read-only tools:

- `get_latest_mission(team, user_id=None)`
- `get_mission_by_id(mission_id)`
- `get_team_matches(team)`
- `search_cities(query, size=5)`
- `get_city_intelligence(city)`
- `search_stadiums(query, size=5)`
- `get_city_stadiums(city)`
- `retrieve_city_candidates(query, size=5)`
- `retrieve_stadium_candidates(query, size=5)`
- `get_alternative_routes(team=None, stage=None, size=5)`
- `get_budget_status(mission_id)`
- `get_preferences(mission_id)`
- `get_replanning_recommendation(mission_id)`

Mutating tools, gated separately:

- `create_mission(team, budget, travel_style, objective, user_id=None)`
- `update_preferences(mission_id, atmosphere_weight, budget_weight, transport_weight)`
- `save_tournament_event(team, event_type, from_stage, to_stage, event_time, source=None)`
- `process_next_tournament_event(team)`
- `run_replanning(mission_id)`

### Query orchestration flow

```text
Agent asks: "Where should I go next for Egypt?"
    |
    v
MCP get_latest_mission(team="Egypt")
    |
    v
MCP retrieve_city_candidates(query)
MCP retrieve_stadium_candidates(query)
MCP get_alternative_routes(...)
    |
    v
Candidate merge/enrichment/scoring service
    |
    v
MCP get_replanning_recommendation(mission_id)
    |
    v
Agent responds with recommendation + reasons + citations
```

### Reasoning flow

```text
Recommendation
    |
    | includes winner, rankings, candidate_source, retrieval_score,
    | score_metadata, contributions
    v
Reasoning builder
    |
    | adds reasons and evidence references
    v
MCP response
    |
    | data + metadata + citations
    v
Agent natural language answer
```

### Citation flow

```text
Elastic hit
    |
    | _index, _id, _score, query, matched source fields
    v
Retrieval candidate metadata
    |
    v
Merged candidate
    |
    v
Recommendation reasoning
    |
    v
citations: [
    {
        "index": "cities",
        "document_id": "Miami",
        "field": "description",
        "score": 3.91,
        "snippet": "Tropical coastal city..."
    }
]
```

## Section 9 - Implementation Plan

### Phase 5.1 - Contracts and hardening

- Create shared Elastic client provider.
- Define schema models for mission, candidate, city, stadium, budget, preference, event, recommendation, and citation.
- Define standard response envelope:

```text
{
    "data": ...,
    "metadata": {
        "source": "...",
        "query": "...",
        "elapsed_ms": ...
    },
    "errors": []
}
```

- Add tool-safe exceptions and error formatting.

### Phase 5.2 - Read-only MCP server prototype

- Expose read-only city, stadium, mission, preference, and retrieval tools.
- Keep all mutating operations out of MCP initially.
- Validate output contracts with deterministic integration tests.
- Add simple observability around tool calls.

### Phase 5.3 - Recommendation MCP tools

- Expose `get_replanning_recommendation`.
- Include rankings, reasoning, contributions, candidate metadata, and score metadata.
- Add citation payloads sourced from retrieval candidates.

### Phase 5.4 - Controlled write tools

- Add preference update tools with optimistic locking.
- Add mission creation tools with user/session scoping.
- Add tournament event tools only after event provenance and retry/dead-letter semantics exist.

### Phase 5.5 - Production readiness

- Add pagination to all search/list tools.
- Add user scoping.
- Add audit logs for MCP calls.
- Add index templates or migrations instead of destructive index scripts.
- Add load/performance tests for wildcard and semantic retrieval.

## Section 10 - Risks

### Technical debt

- Repeated module-level Elasticsearch client creation.
- Raw dicts instead of typed contracts.
- Mixed test/setup scripts and production service assumptions.
- Duplicate agent definitions.
- Inconsistent error handling.

### Migration risks

- Introducing MCP before stable contracts could freeze unstable raw dict shapes.
- Adding citations later will be harder if retrieval provenance is not added before MCP response schemas are published.
- Write tools could mutate mission/preference state unexpectedly without gating.

### Performance risks

- Wildcard queries on keyword fields can become expensive.
- `alternative_routes` uses `match_all`, which will not scale.
- Several list operations use fixed `size=100` or no explicit pagination.
- Candidate generation fans out into multiple Elastic calls per replanning request.

### Scaling risks

- Team-only mission lookup is insufficient for multi-user usage.
- City/stadium IDs are human-readable names and may collide.
- No recommendation history index exists, so longitudinal explainability is limited.
- Event duplicate protection is timestamp-sensitive.

### Explainability risks

- Reasoning now names source and score metadata but does not cite evidence documents.
- Retrieval scores are Elastic query scores, not calibrated confidence.
- Semantic retrieval currently uses lexical/fuzzy search, not vector semantic search.

## Summary Recommendation

Scout should proceed with a read-only Elastic MCP prototype after P0 hardening. The best first MCP tools are city/stadium retrieval, mission read, preference read, and replanning recommendation read. Mutating tools should wait until user scoping, optimistic locking coverage, and tool permission boundaries are explicit.

Recommended readiness gate:

- Read-only MCP: acceptable after P0 items 1-4.
- Mutating MCP: wait for P0 item 5 and P1 user/concurrency/audit work.
- Production MCP: wait for pagination, provenance, citations, and non-destructive index management.
