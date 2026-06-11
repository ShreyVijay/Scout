# Scout Production Deployment Runbook

## 1. Create the GitLab Repository

1. In GitLab, create a blank private project named `Scout`.
2. Protect the default branch.
3. Require successful pipelines before merge.
4. Add the GitLab remote locally: `git remote add gitlab <gitlab-repository-url>`.
5. Confirm no real `.env` files or credentials are tracked: `git status --ignored`.

## 2. Push the Project

1. Review all changes.
2. Commit the deployment files.
3. Push the default branch: `git push -u gitlab <default-branch>`.
4. Confirm lint, test, and build stages pass.

## 3. Configure Variables

In GitLab **Settings > CI/CD > Variables**, add masked/protected production values:

- `ELASTIC_CLOUD_ID`, `ELASTIC_USERNAME`, `ELASTIC_PASSWORD`
- `GEMINI_API_KEY` when the agent runtime is enabled
- `RAILWAY_DEPLOY_HOOK_URL`, `VERCEL_DEPLOY_HOOK_URL`, and `PRODUCTION_URL` for managed hosting
- `SSH_PRIVATE_KEY`, `DEPLOY_HOST`, `DEPLOY_USER`, and `DEPLOY_PATH` only for the optional Compose deployment job

In the frontend host, add `VITE_API_BASE_URL=<public-backend-url>`. Add `VITE_GOOGLE_MAPS_API_KEY` only after restricting it by allowed production domains.

## 4. Deploy the Backend to Railway

1. Create a Railway project and service.
2. Choose deployment from Dockerfile with root directory `backend`.
3. Add `ELASTIC_CLOUD_ID`, `ELASTIC_USERNAME`, `ELASTIC_PASSWORD`, `CORS_ORIGINS`, and `WEB_CONCURRENCY=2`.
4. Set `CORS_ORIGINS` to the exact Vercel production URL.
5. Configure the healthcheck path as `/health`.
6. Deploy and record the generated HTTPS backend URL.
7. Verify `GET <backend-url>/health` returns `{"status":"ok"}`.
8. Verify `GET <backend-url>/readiness` returns `{"status":"ready"}`.
9. Create a Railway production deploy hook and store it in GitLab as `RAILWAY_DEPLOY_HOOK_URL`.

## 5. Deploy the Frontend to Vercel

1. Import the GitLab repository into Vercel.
2. Set the root directory to `frontend`.
3. Set build command to `npm run build`.
4. Set output directory to `dist`.
5. Add `VITE_API_BASE_URL=<railway-backend-url>`.
6. Deploy and record the production URL.
7. Update backend `CORS_ORIGINS` to that exact URL and redeploy backend.
8. Create a Vercel production deploy hook and store it in GitLab as `VERCEL_DEPLOY_HOOK_URL`.
9. Disable provider-side automatic production deployments so GitLab remains the deployment orchestrator.
10. Run the manual `deploy_managed_production` GitLab job for subsequent deployments.

## 6. Verify Elasticsearch

1. Create a least-privilege Elastic service user for Scout.
2. Put its values in Railway, never Vercel.
3. Call backend `/readiness`; require HTTP `200` and `{"status":"ready"}`.
4. Call `/cities`, `/stadiums`, and a known mission endpoint.
5. If indices are absent, run the existing index/data ingestion scripts from a controlled admin environment with the same Elastic credentials.

## 7. Verify APIs

```bash
curl <backend-url>/health
curl <backend-url>/readiness
curl <backend-url>/cities
curl <backend-url>/stadiums
curl <backend-url>/travel/flights
```

Do not approve production while readiness is `503`.

## 8. Verify Frontend-Backend Communication

1. Open the Vercel production URL.
2. In browser developer tools, confirm API requests target the Railway URL.
3. Confirm no CORS errors occur.
4. Load cities/stadiums and execute a known mission flow.
5. Confirm no secrets appear in the browser bundle or network responses.

## 9. Rollback Strategy

1. Identify the last known-good GitLab commit and provider deployment.
2. In Vercel, promote the last known-good deployment.
3. In Railway, roll back to the last known-good deployment.
4. If using the VPS job, check out the known-good commit on the host and run `docker compose up -d --build`.
5. Verify `/health`, `/readiness`, and the frontend mission flow.
6. Do not roll back Elastic data destructively; restore from a verified Elastic snapshot when required.
