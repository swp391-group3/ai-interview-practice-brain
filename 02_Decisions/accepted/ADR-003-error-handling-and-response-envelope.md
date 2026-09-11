---
project: SEP490
type: decision
status: accepted
authority: team
last_verified: 2026-09-11
---

# ADR-003: Structured Application Errors and Standardized HTTP Response Envelope

## 1. Status
`ACCEPTED` (Implemented in `api/pkg/apperror` and `api/pkg/response`)

## 2. Context & Problem Statement
Without a unified error model and response structure, REST API endpoints return inconsistent error payloads, making client-side error handling and UI feedback fragile and ad-hoc.

## 3. Decision Drivers
- Uniform client-side decoding in `frontend/src/lib/api/`.
- Clear differentiation between domain errors (e.g., `invalid_credentials`, `account_locked`) and unexpected 500 internal errors.
- Prevention of sensitive internal database or stack trace leakage to clients.

## 4. Decision Outcome
Every HTTP response from `api/` adheres to the standardized envelope:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```
Or upon failure:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "validation_error",
    "message": "Detailed description"
  }
}
```

### Components
1. `api/pkg/apperror`: Defines domain `Code` types and `AppError` struct.
2. `api/pkg/response`: Provides `response.OK()`, `response.Created()`, and `response.Error()` helper functions mapping `apperror.Code` directly to appropriate HTTP status codes.
