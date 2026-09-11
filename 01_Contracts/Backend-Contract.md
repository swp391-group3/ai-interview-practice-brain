---
project: SEP490
type: contract
status: accepted
authority: code
last_verified: 2026-09-11
---

# Backend Engineering Contract

## 1. Status & Metadata
- **Status:** `ACCEPTED` (Enforced by current code in `api/`)
- **Root Directory:** `api/`
- **Runtime:** Go 1.27
- **Web Framework:** Gin v1.12.0
- **Database Engine:** PostgreSQL 16+ via `pgx/v5` connection pool

## 2. Package Architecture
All backend application logic resides under `api/`:
```
api/
├── cmd/http/main.go               # Server initialization and graceful shutdown
├── internal/
│   ├── auth/                      # Authentication domain (repository, service, transport)
│   ├── jd/                        # Job description domain (planned KAN-18, KAN-19)
│   └── shared/                    # Shared configuration and HTTP router assembly
├── migration/                     # Schema migrations (000001_init.up.sql)
└── pkg/
    ├── apperror/                  # Standard error codes & wrapping
    ├── response/                  # Unified JSON HTTP envelope
    ├── token/                     # JWT signing and claim validation
    └── util/                      # Database pool lifecycle
```

## 3. Architectural Invariants
- **No Clean Architecture Boilerplate:** Do not create separate `usecase/`, `domain/`, `interfaces/` layers per service unless approved. Co-locate feature logic in `internal/<domain>/`.
- **No ORM Reflection:** Database queries MUST use `sqlc` compiled Go methods over raw `pgx/v5`. GORM is prohibited.
- **Strict SQL Migrations:** All schema changes must be versioned sequential files (`NNNNNN_name.up.sql` and `NNNNNN_name.down.sql`).
- **Response Envelope Uniformity:** All HTTP endpoints must return payloads via `pkg/response` (`response.OK`, `response.Created`, `response.Error`).
- **Domain Errors:** Errors passed to HTTP layer must be wrapped as `*apperror.AppError` with a defined `apperror.Code`.

## 4. Open Questions
- OQ-04: Multi-package `sqlc.yaml` generation pattern for `internal/jd/repository` (see [[Open-Questions]]).

## 5. Traceability
- **Relevant ADRs:** [[ADR-001-backend-directory-and-package-structure]], [[ADR-002-database-access-sqlc-pgx]], [[ADR-003-error-handling-and-response-envelope]]
- **Relevant Code:** `api/cmd/http/main.go`, `api/sqlc.yaml`, `api/pkg/apperror/apperr.go`, `api/pkg/response/response.go`
