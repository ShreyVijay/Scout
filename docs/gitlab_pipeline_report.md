# GitLab Pipeline Report

The root `.gitlab-ci.yml` defines:

1. `lint`: Python compilation and frontend ESLint.
2. `test`: backend health/readiness unit tests and a frontend production build validation.
3. `build`: downloadable backend package/wheels and frontend `dist/` artifacts.
4. `deploy`: protected, manual jobs for the recommended managed hosts or a Docker Compose VPS.

## Required Deploy Variables

- `SSH_PRIVATE_KEY`: masked/protected private key accepted by the deployment host.
- `DEPLOY_HOST`: production host name or IP.
- `DEPLOY_USER`: restricted deployment user.
- `DEPLOY_PATH`: absolute repository path on the host.
- `PRODUCTION_URL`: environment URL shown by GitLab.
- `RAILWAY_DEPLOY_HOOK_URL`: Railway production service deploy hook.
- `VERCEL_DEPLOY_HOOK_URL`: Vercel production deploy hook.

Use `deploy_managed_production` for Vercel + Railway or `deploy_vps_production` for Compose. Keep deployment manual until the first production deployment and rollback have both been verified. Then change the selected job's rule from `when: manual` to an approved automatic policy.
