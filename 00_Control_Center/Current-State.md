---
project: SEP490
type: control
status: current
authority: local-brain
last_verified: 2026-09-18
---

# Current Project State

## Snapshot

PR #15 merged at `97abe3bf9eadb92051b8a8b5337ea62d0ecbe565`; local `main` has subsequently advanced with landing-page work. The backend is feature-oriented under `api/internal/features`, with Go 1.27, Gin, PostgreSQL/pgx, sqlc, Viper, Zap, OpenTelemetry, and Wire. Merged JD extraction (KAN-18) uses Eino with a Gemini-backed configured model; merged auth exposes `/auth/login`, returns an access token, and sets a refresh cookie.

## Authority-separated JD state

- **MERGED IMPLEMENTATION:** PR #14 tooling/foundation; KAN-18 extraction; PR #15 reviewed JD repository, authenticated `/jds` API, Swagger, feature-local sqlc, and `interview_blueprints` migration.
- **JIRA / DESIRED STATE:** KAN-18, KAN-19, and KAN-46 are Done; KAN-20, KAN-44, and KAN-45 are In Progress. KAN-19 Jira and merged-code state now align.

## Frontend

Frontend remains Next.js 16 / React 19 with custom fetch transport, TanStack Query, Zustand, React Hook Form, and Zod. Direct inspection found the JD UI remains a placeholder; do not infer KAN-20 implementation from its Jira status.

## Current gaps

- PDF ingestion library/pipeline (KAN-44) remains unverified/open.
- Evaluation dataset (KAN-45) remains in progress.
- Blueprint target model is not fully implemented: merged migration creates `interview_blueprints`, but does not re-parent sessions or establish all blueprint business rules.
- Role enum `participant`, `jury`, `admin` still differs from product language.
