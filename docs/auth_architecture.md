# Scout Future Authentication Architecture Design

This document details the architecture design for implementing user authentication in future releases of Scout.

---

## 1. Authentication Methods

Scout will support three primary authentication methods:

### Google OAuth 2.0
* **Flow**: Authorization Code Flow with PKCE (Proof Key for Code Exchange) for secure single-page React client login.
* **Mechanism**:
  1. Frontend redirects user to Google Consent screen:
     ```text
     https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...&response_type=code&scope=openid%20email%20profile
     ```
  2. Google redirects back to `/auth/callback` on the frontend with an authorization code.
  3. Frontend sends authorization code to backend endpoint `POST /api/v1/auth/google`.
  4. Backend exchanges code for ID/Access tokens, queries profile info, updates/creates User document in Elasticsearch, and issues a stateless JWT session cookie.

### Email + Password
* **Flow**: Traditional credentials login.
* **Mechanism**:
  1. User registers/logs in via `POST /api/v1/auth/register` or `POST /api/v1/auth/login`.
  2. Passwords are encrypted using **bcrypt** (salt rounds = 12) before being written to Elasticsearch.
  3. Elasticsearch schema will store a `password_hash` field (never returned in API responses).
  4. Upon successful login, backend returns a JWT session.

### Magic Link (Passwordless)
* **Flow**: Secure, passwordless access.
* **Mechanism**:
  1. User enters email at `/login` and triggers magic link request: `POST /api/v1/auth/magic-link`.
  2. Backend generates a high-entropy cryptographically secure token (valid for 15 minutes, single-use).
  3. Backend saves hash of token in memory cache (e.g. Redis) and emails the magic link to the user:
     ```text
     https://scout-travel.fan/login/verify?token=SECURE_HEX_TOKEN
     ```
  4. User clicks the link; frontend sends token to `POST /api/v1/auth/magic-link/verify`, generating a session.

---

## 2. Session Management & Tokens

Scout will use stateless **JSON Web Tokens (JWT)** for session control.

### JWT Structure
* **Payload**:
  ```json
  {
    "sub": "user_id_123456",
    "email": "fan@fifa2026.com",
    "name": "Super Fan",
    "role": "fan",
    "exp": 1781222400
  }
  ```

### Storage and Transport
* **HTTP-Only Cookies**: JWTs will be stored in secure, `HttpOnly`, `SameSite=Lax`, and `Secure` (production-only) cookies. This completely mitigates XSS-based token theft.
* **CORS & Domain Policy**: API requests will set `credentials: 'include'` on Axios instance to automatically attach the session cookie.

---

## 3. Storage Schema Integration

The `users` index mapping in Elasticsearch will expand to support authentication:

```json
{
  "user_id": "keyword",
  "email": "keyword",
  "name": "text",
  "password_hash": "keyword",
  "auth_provider": "keyword",  // "google", "local", "magic_link"
  "preferences": {
    "properties": {
      "atmosphere_weight": "float",
      "budget_weight": "float",
      "transport_weight": "float"
    }
  },
  "saved_missions": "keyword",
  "created_at": "date",
  "updated_at": "date"
}
```
