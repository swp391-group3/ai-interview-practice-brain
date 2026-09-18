---
project: SEP490
type: contract
status: current
authority: code
last_verified: 2026-09-18
---

# API Contract & Transport Protocol

## Authority boundary

- **MERGED IMPLEMENTATION (`main`):** `GET /health`, `POST /auth/login`, response envelope, access-token middleware, refresh-cookie login behavior, `/jds` routes, JD persistence mappings, and `/swagger/*any`.

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

| Code | HTTP status in merged `main` | Merged PR #15 mapping |
|---|---:|---:|
| `INVALID_CREDENTIALS`, `INVALID_TOKEN` | 401 | 401 |
| `USER_NOT_FOUND` | 404 | 404 |
| `USER_INACTIVE` | 403 | 403 |
| `VALIDATION_ERROR`, `INVALID_JD_INPUT`, `JD_TOO_SHORT`, `JD_TOO_LONG` | 400 (where registered) | 400 |
| `EXTRACTION_FAILED`, `INVALID_EXTRACTION_OUTPUT` | 502 | 502 |
| `INTERNAL_ERROR` | 500 | 500 |
| `JD_NOT_FOUND` | 404 | 404 |
| `JD_IN_USE` | 409 | 409 |

All codes are uppercase stable strings.

## Merged JD route surface — PR #15

All require Bearer authentication:

| Method | Route | Semantics |
|---|---|---|
| POST | `/jds/analyze` | Analyze raw text without saving |
| POST | `/jds` | Persist a reviewed JD; returns 201 envelope |
| GET | `/jds` | List caller-owned JDs; paginated |
| GET | `/jds/:id` | Fetch a caller-owned JD |
| PUT | `/jds/:id` | Update reviewed structured fields; raw text stays immutable |
| DELETE | `/jds/:id` | Delete caller-owned JD; returns 204 on success |

`/swagger/*any` is merged Swagger infrastructure. List uses `limit` (default 20, 1–100) and `offset` (default 0); data contains `items` plus `pagination.limit`, `pagination.offset`, and `pagination.total`. Public JD responses do not expose `userId`. Stale `/api/v1/jd/upload` and `/api/v1/jd/:id/blueprint` proposals are superseded, not current routes.

## Configuration

Server port is configurable. `main` configuration defaults to `3000`; it is not a permanent `8080` contract.
