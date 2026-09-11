---
project: SEP490
type: contract
status: current
authority: code
last_verified: 2026-09-11
---

# API Contract & Transport Protocol

## 1. Status & Metadata
- **Status:** `CURRENT` (Reflects merged implementation in `api/` and `frontend/`)
- **Base Protocol:** REST over HTTP/1.1 or HTTP/2
- **Data Serialization:** JSON (UTF-8)
- **Default Port:** `8080`

## 2. Standard JSON Response Envelope
Every HTTP endpoint returns the canonical envelope format:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

### Failure Response
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "invalid_credentials",
    "message": "email or password is not correct"
  }
}
```

## 3. Error Code Registry (`api/pkg/apperror`)
| Error Code | HTTP Status | Description |
| :--- | :--- | :--- |
| `invalid_credentials` | 401 Unauthorized | Email/password verification failure |
| `invalid_token` | 401 Unauthorized | Expired, malformed, or invalid signature JWT |
| `account_locked` | 403 Forbidden | Account is disabled or suspended by Admin |
| `account_not_found` | 404 Not Found | Requested user account does not exist |
| `validation_error` | 400 Bad Request | Payload schema or validation constraint failure |
| `internal_error` | 500 Internal Server Error | Unhandled server error |

## 4. Implemented Endpoints
| Method | Route Path | Auth Required | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/auth/login` | No | Authenticate user credentials, return JWT access/refresh token pair | `IMPLEMENTED` (*Path has nested prefix bug*) |

## 5. Planned Endpoints (JD Domain — KAN-19)
| Method | Route Path | Auth Required | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/jd/upload` | Yes (Bearer) | Ingest PDF file or raw text, trigger extraction | `PLANNED` |
| `GET` | `/api/v1/jd/:id` | Yes (Bearer) | Retrieve extracted JD details & requirements | `PLANNED` |
| `PUT` | `/api/v1/jd/:id` | Yes (Bearer) | Save candidate edits to extracted skills/requirements | `PLANNED` |
| `POST` | `/api/v1/jd/:id/blueprint`| Yes (Bearer) | Generate & return structured interview blueprint | `PLANNED` |

## 6. Known Discrepancies
- In `api/internal/auth/transport/http/server.go`, the login route is mounted as `/auth/auth/login`. This will be corrected to `/auth/login` or `/api/v1/auth/login`.
