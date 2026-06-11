# Environment Configuration Report

Never commit `.env` files or place secrets in Vite variables. Every `VITE_*` value is embedded into the public browser bundle.

## Backend Variables

| Variable | Required | Purpose |
|---|---:|---|
| `PORT` | Hosting-dependent | FastAPI listen port; defaults to `8000`. |
| `WEB_CONCURRENCY` | No | Uvicorn worker count; defaults to `2`. |
| `CORS_ORIGINS` | Yes | Comma-separated allowed frontend origins. |
| `ELASTIC_CLOUD_ID` | Yes | Elastic Cloud deployment identifier. |
| `ELASTIC_USERNAME` | Yes | Elastic service user. |
| `ELASTIC_PASSWORD` | Yes | Elastic service-user password. |
| `GEMINI_API_KEY` | Agent only | Gemini/Google ADK access. |

Future provider placeholders are listed in `backend/.env.example`: Amadeus, Skyscanner, Kiwi, Booking, Expedia, FlixBus, Ticketmaster, StubHub, and SeatGeek.

## Frontend Variables

| Variable | Required | Purpose |
|---|---:|---|
| `VITE_API_BASE_URL` | Yes | Public backend base URL, or `/api` behind nginx. |
| `VITE_GOOGLE_MAPS_API_KEY` | No | Browser Maps API key; restrict by HTTP referrer. |

## Secret Handling

- Local/Compose: create `.env` from `.env.example`.
- GitLab: store secrets as masked and protected CI/CD variables.
- Hosting providers: store backend secrets in provider secret/environment settings.
- Rotate Elastic credentials immediately if they have ever appeared in source or logs.
