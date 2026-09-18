---
project: SEP490
type: control
status: current
authority: local-brain
last_verified: 2026-09-18
---

# Current Project State

## Snapshot

`main` is at merge commit `bfdc9cc4` (PR #13 backend refactor). The backend is feature-oriented under `api/internal/features`, with Go 1.27, Gin, PostgreSQL/pgx, sqlc, Viper, Zap, OpenTelemetry, and Wire. Merged JD extraction (KAN-18) uses Eino with a Gemini-backed configured model; merged auth exposes `/auth/login`, returns an access token, and sets a refresh cookie.

## Authority-separated JD state

- **MERGED IMPLEMENTATION:** structured JD extraction exists at `api/internal/features/jd`; no JD REST/persistence routes are merged.
- **OPEN PR / WORKING IMPLEMENTATION:** PR #14 `chore/backend-foundation` adds backend foundation/tooling work. PR #15 `feature/jd-api` adds JD repository, `/jds` API, Swagger, sqlc JD configuration, and `interview_blueprints` migration. Local branch is 16 commits ahead of `main`, but it is not merged.
- **JIRA / DESIRED STATE:** KAN-18, KAN-19, and KAN-46 are Done; KAN-20, KAN-44, and KAN-45 are In Progress. KAN-19 Done versus PR #15 open is a deliberate authority discrepancy.

## Frontend

Frontend remains Next.js 16 / React 19 with custom fetch transport, TanStack Query, Zustand, React Hook Form, and Zod. Direct inspection found the JD UI remains a placeholder; do not infer KAN-20 implementation from its Jira status.

## Current gaps

- PDF ingestion library/pipeline (KAN-44) remains unverified/open.
- Evaluation dataset (KAN-45) remains in progress.
- Blueprint target model is not fully implemented: PR #15 creates `interview_blueprints`, but does not re-parent sessions or establish all blueprint business rules.
- Role enum `participant`, `jury`, `admin` still differs from product language.
