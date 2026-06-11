# Health Check Report

## Endpoints

### `GET /health`

Liveness endpoint. It does not contact dependencies.

```json
{"status": "ok"}
```

### `GET /readiness`

Readiness endpoint. It verifies `ELASTIC_CLOUD_ID`, `ELASTIC_USERNAME`, and `ELASTIC_PASSWORD`, then pings Elastic Cloud.

Successful response:

```json
{"status": "ready"}
```

Missing variables or failed Elastic connectivity return HTTP `503` with non-secret diagnostic check status.

## Usage

Use `/health` for container/process restarts. Use `/readiness` for deployment verification and load-balancer admission.
