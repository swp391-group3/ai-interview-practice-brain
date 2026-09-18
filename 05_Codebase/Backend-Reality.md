---
project: SEP490
type: code-reality
status: current
authority: code
last_verified: 2026-09-18
---

# Backend Implementation Reality

## MERGED IMPLEMENTATION (`main`)

Go 1.27 backend at `api/`: Gin, PostgreSQL with pgx/v5, sqlc, numbered migrations, Viper config (default server port `3000`), Zap logger, OpenTelemetry tracer, and Wire DI. The entrypoint is `api/cmd/api`, not `cmd/http`.

Auth is in `api/internal/features/auth`; `/auth/login` works (the nested route bug is fixed). It issues access and refresh JWTs using separate secrets, returns the access token in the response envelope, and writes refresh token cookie `refresh` at `/auth/refresh`. `middleware.RequireAuth` validates Bearer access tokens and exposes the UUID via `CurrentUserID`.

JD extraction exists in `api/internal/features/jd`: Eino sends an exact structured JSON request through the configured Gemini model, then deterministic validation enforces the current technical-competency contract. LLM and provider absence are no longer valid claims.

## Merged PR #14 / #15 reality

PR #14 merged config/lifecycle, Air, CORS/logging, Swagger, Testcontainers, Makefile and review-workflow changes. Config file port is 3000 while Makefile local commands fall back to 8080 when `SERVER_PORT` is absent.

PR #15 merged feature-local JD repository/sqlc code, authenticated `/jds` handlers, Swagger, integration tests, `JD_NOT_FOUND`/`JD_IN_USE`, and migration 000002. `GET /jds` is paginated and response DTOs omit `userId`.

## Not verified as implemented

PDF ingestion, JD evaluation dataset, interview runtime/FSM, avatar/audio processing, Redis, and full target blueprint/session schema remain absent or unverified. Do not call the target ERD current database reality.
