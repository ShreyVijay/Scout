# Dockerization Report

## Implemented

- `backend/Dockerfile`: Python 3.13 slim, non-root runtime user, pinned dependency install, Uvicorn production command, configurable workers/port, liveness healthcheck.
- `frontend/Dockerfile`: Node 22 multi-stage Vite build and nginx static runtime.
- `frontend/nginx.conf`: SPA fallback and `/api/` reverse proxy to the backend service.
- `docker-compose.yml`: backend/frontend services, restart policies, environment injection, healthchecks, and dependency ordering.
- `.dockerignore` files prevent secrets, local dependencies, tests, and build output from entering images.

## Commands

```bash
cp .env.example .env
docker compose config
docker compose up -d --build
docker compose ps
```

The backend liveness check is `/health`. Use `/readiness` separately to verify Elastic Cloud credentials and connectivity.
