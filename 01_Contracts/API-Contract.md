---
project: SEP490
type: contract
status: current
authority: code
last_verified: 2026-09-18
---

# API Contract & Transport Protocol

## Authority boundary

- **MERGED IMPLEMENTATION (`main`):** `GET /health`, `POST /auth/login`, response envelope, access-token middleware, and refresh-cookie login behavior.
- **OPEN PR / WORKING IMPLEMENTATION (PR #15, `feature/jd-api`):** `/jds` routes, JD persistence mappings, `JD_NOT_FOUND`/`JD_IN_USE`, and `/swagger/*any`. These are not merged API commitments.

## Wire format — ACCEPTED CONTRACT

`response.Envelope` uses `omitempty`; successful and failed JSON responses respectively serialize conceptually as:

```json
{"success":true,"data":{}}
```

```json
{"success":false,"error":{"code":"VALIDATION_ERROR","message":"..."}}
```

Do not require `data: null` or `error: null`. A successful DELETE in PR #15 is `204 No Content`, with no envelope.

## Merged routes

| Method | Route | Auth | Reality |
|---|---|---|---|
| GET | `/health` | No | **MERGED IMPLEMENTATION** health response |
| POST | `/auth/login` | No | **MERGED IMPLEMENTATION**; returns access token in `data`, sets refresh cookie |

The historical nested `/auth/auth/login` route is fixed and must not be used.

### Authentication boundary

Protected routes use `Authorization: Bearer <access-token>`. Middleware validates with the access secret and stores the authenticated UUID in Gin context; handlers retrieve it through `middleware.CurrentUserID`. Login uses distinct access and refresh JWT secrets. The refresh cookie is named `refresh` and currently has path `/auth/refresh`; no additional cookie attributes should be inferred from code.

## Error registry

| Code | HTTP status in merged `main` | PR #15 working mapping |
|---|---:|---:|
| `INVALID_CREDENTIALS`, `INVALID_TOKEN` | 401 | 401 |
| `USER_NOT_FOUND` | 404 | 404 |
| `USER_INACTIVE` | 403 | 403 |
| `VALIDATION_ERROR`, `INVALID_JD_INPUT`, `JD_TOO_SHORT`, `JD_TOO_LONG` | 400 (where registered) | 400 |
| `EXTRACTION_FAILED`, `INVALID_EXTRACTION_OUTPUT` | not mapped to 502 in `main` | 502 |
| `INTERNAL_ERROR` | 500 | 500 |
| `JD_NOT_FOUND` | absent | 404 |
| `JD_IN_USE` | absent | 409 |

All codes are uppercase stable strings. The PR #15 mappings remain **OPEN PR / WORKING IMPLEMENTATION**.

## PR #15 route surface — OPEN PR / WORKING IMPLEMENTATION

All require Bearer authentication:

| Method | Route | Semantics |
|---|---|---|
| POST | `/jds/analyze` | Analyze raw text without saving |
| POST | `/jds` | Persist a reviewed JD; returns 201 envelope |
| GET | `/jds` | List caller-owned JDs |
| GET | `/jds/:id` | Fetch a caller-owned JD |
| PUT | `/jds/:id` | Update reviewed structured fields; raw text stays immutable |
| DELETE | `/jds/:id` | Delete caller-owned JD; returns 204 on success |

`/swagger/*any` is also open-PR Swagger infrastructure. Stale `/api/v1/jd/upload` and `/api/v1/jd/:id/blueprint` proposals are superseded, not current routes.

## Configuration

Server port is configurable. `main` configuration defaults to `3000`; it is not a permanent `8080` contract.
