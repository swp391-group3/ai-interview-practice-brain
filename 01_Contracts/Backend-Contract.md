---
project: SEP490
type: contract
status: accepted
authority: code
last_verified: 2026-09-18
---

# Backend Engineering Contract

## ACCEPTED CONTRACT — merged architecture

The backend root is `api/`, using Go 1.27, Gin, PostgreSQL with `pgx/v5`, sqlc, numbered SQL migrations, centralized application errors, and the `response.Envelope` boundary. Configuration is Viper-based; logging is Zap-based and tracing uses OpenTelemetry. Google Wire supplies compile-time dependency injection.

```text
api/
├── cmd/api/                         # application entrypoint and Wire output
├── internal/config/                 # Viper config
├── internal/database/               # pgx pool
├── internal/features/auth/          # feature repository + service
├── internal/features/jd/            # merged extraction feature
├── internal/handler/                # Gin handlers
├── internal/middleware/             # auth, CORS, logging, recovery
├── internal/provider/               # Wire providers
├── internal/router/                 # route assembly
├── internal/server/                 # HTTP lifecycle
├── internal/pkg/{ai,logger,tracer}/ # internal infrastructure adapters
├── migration/                       # numbered up/down migrations
└── pkg/{apperror,response,token}/   # shared public packages
```

Do not revive the legacy `cmd/http`, `internal/auth`, `internal/shared`, `pkg/util`, or planned `internal/jd` model.

## Engineering invariants

- Use sqlc-generated pgx/v5 access; no GORM assumption.
- Version schema changes as numbered `.up.sql` / `.down.sql` migrations.
- Return handled JSON through `response.OK`, `response.Created`, or `response.Error` except intentional no-content responses.
- Surface known failures as `*apperror.AppError` with a stable uppercase code.
- Feature code is organized beneath `internal/features/<feature>`; router/handler/provider infrastructure remains outside feature packages.

## OPEN PR / WORKING IMPLEMENTATION

PR #14 (`chore/backend-foundation`) adds/changes Air, lifecycle/config stabilization, CORS/request logging, Swagger, PostgreSQL Testcontainers, Makefile targets, and review tooling. PR #15 also carries Swagger and tests. These are not merged guarantees until their branch merges.

PR #15 has a two-entry `api/sqlc.yaml` for `internal/features/auth/repository` and `internal/features/jd/repository`; this resolves the working layout but remains pending merge.

## Verification pointers

`api/go.mod`, `api/cmd/api/`, `api/internal/{config,database,handler,middleware,provider,router,server}/`, `api/pkg/{apperror,response}/`, and `api/sqlc.yaml`.
