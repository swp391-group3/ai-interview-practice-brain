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

## Merged tooling foundation

Merged PR #14 adds/changes Air, lifecycle/config stabilization, CORS/request logging, Swagger, PostgreSQL Testcontainers, Makefile targets, and on-demand OpenCode review tooling. PR #15 merged the JD persistence/API additions.

`api/sqlc.yaml` has entries for `internal/features/auth/repository` and `internal/features/jd/repository`.

`configs/config.yaml` defaults `server.port` to `3000`; `make run` and `make dev` fall back to `SERVER_PORT=8080` only when the root environment omits it. Neither is a universal permanent port.

## Verification pointers

`api/go.mod`, `api/cmd/api/`, `api/internal/{config,database,handler,middleware,provider,router,server}/`, `api/pkg/{apperror,response}/`, and `api/sqlc.yaml`.
