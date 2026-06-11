# Production Hosting Recommendation

**Recommendation: Option A, Vercel frontend + Railway backend.**

Pricing checked June 11, 2026. Verify again before purchase.

| Option | Cost starting point | Complexity | Speed to production | Reliability |
|---|---|---|---|---|
| A: Vercel + Railway | Vercel Hobby is free for personal use; Pro is $20/month. Railway Hobby has a $5 minimum with usage credit; Pro has a $20 minimum. | Low | Fastest | Railway lists 99.9% Hobby and 99.99% Pro availability targets. |
| B: Vercel + Render | Vercel as above; Render web service Starter is $7/month, Standard is $25/month. | Low | Fast | Managed health checks, deploys, and rollbacks; small free services are not production-grade. |
| C: Docker Compose VPS | A DigitalOcean basic Droplet starts at $6/month for 1 GiB or $12/month for 2 GiB. | High | Moderate | Reliability, patching, TLS, backups, monitoring, and failover are operator-owned. |

Option A best matches the immediate-production goal: Vercel is excellent for a Vite SPA, Railway deploys the FastAPI Docker image quickly, and both keep operational work low. Use paid production tiers, configure spend limits, and keep GitLab CI as the required test/build gate.

Official pricing sources:

- https://vercel.com/pricing
- https://railway.com/pricing
- https://render.com/pricing
- https://www.digitalocean.com/pricing/droplets
