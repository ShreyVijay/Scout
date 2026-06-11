# Scout Deployment Audit

**Audit date:** June 11, 2026

## 1. Current Architecture

- `frontend/`: React 19 SPA built by Vite, React Router client-side routing, Axios API client, optional Google Maps browser integration.
- `backend/`: FastAPI application served from `main:app`; synchronous service layer; Elastic Cloud is the primary datastore.
- Gemini: ADK agent modules exist, but the FastAPI application does not currently expose or initialize them.
- MCP: read-only MCP tool wrappers and a standalone MCP server exist. MCP is not mounted into the FastAPI runtime.
- Travel providers: mock provider implementations behind provider-shaped service modules.

## 2. Missing Deployment Files Found

At audit start the repository had no Dockerfiles, Compose file, nginx configuration, GitLab pipeline, environment examples, health endpoints, or deployment runbook. These are now supplied.

## 3. Required Environment Variables

Production-required:

- `ELASTIC_CLOUD_ID`
- `ELASTIC_USERNAME`
- `ELASTIC_PASSWORD`
- `CORS_ORIGINS`
- `VITE_API_BASE_URL`

Integration-dependent:

- `GEMINI_API_KEY`
- `VITE_GOOGLE_MAPS_API_KEY`
- Future travel-provider keys documented in `backend/.env.example`

## 4. Build Blockers

- The frontend source is JSX, but `npm run build` previously ran `tsc -b`; `tsconfig.app.json` found no TypeScript inputs and failed. The production build now runs Vite directly.
- `backend/requirements.txt` omitted `elasticsearch`, although most operational services import it. The dependency is now declared.
- Backend tests are mostly executable integration scripts and many require live Elastic credentials. A deterministic health/readiness unit test is now used by CI.

## 5. Runtime Blockers

- Production readiness remains blocked until valid Elastic Cloud credentials are configured.
- Elastic clients are widely created at module import time. This is existing architecture and increases failure/cold-start risk, but was not refactored due to scope.
- Gemini and MCP SDK dependencies are not declared in the production API requirements because neither is imported by FastAPI startup. Their standalone runtimes require separate dependency packaging before deployment.
- Existing data indices must be initialized before business APIs can return useful results.

## 6. Deployment Risks

- No authentication/authorization protects current APIs.
- Several endpoints return raw exception text.
- API tests do not cover the main business workflows in an isolated environment.
- Frontend lint configuration primarily targets TypeScript while the active source is JSX.
- No centralized metrics, error tracking, backups verification, rate limiting, or automated rollback exists.
- A single backend service and synchronous Elastic calls limit resilience under load.

## 7. Recommended Hosting Architecture

Use **Vercel for the frontend and Railway for the FastAPI backend**, with Elastic Cloud retained as the datastore. GitLab CI remains the quality gate and deployment orchestrator; the included manual VPS deployment job is a bootstrap path until provider deployment tokens/hooks are configured.
