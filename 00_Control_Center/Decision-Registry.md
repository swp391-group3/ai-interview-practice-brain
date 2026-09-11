---
project: SEP490
type: decision
status: current
authority: team
last_verified: 2026-09-11
---

# Architecture & Engineering Decision Registry

> [!NOTE]
> This registry records all technical, architectural, and product decisions across SEP490.
> **Rule:** Never infer `ACCEPTED` status without verifiable evidence (ADR, merged code, or explicit team agreement). Unresolved choices remain `OPEN`, `PROPOSED`, or `SPIKE`.

---

## 1. Decision States Summary

| Status | Meaning |
| :--- | :--- |
| **ACCEPTED** | Ratified team decision, merged code standard, or approved ADR. |
| **PROPOSED** | Formal proposal submitted for team review, not yet agreed. |
| **OPEN** | Architectural question under active exploration with no decision. |
| **SPIKE** | Timeboxed proof-of-concept / research experiment. |
| **SUPERSEDED**| Previously accepted decision replaced by a newer decision. |
| **DEPRECATED**| Retained temporarily but slated for decommissioning. |
| **REJECTED**  | Considered and explicitly declined. |

---

## 2. Master Decision Log

| Area | Decision Summary | State | Evidence / Authority | Date | Supersedes | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Backend Core** | Backend code root placed at `api/` (not `backend/`) | `ACCEPTED` | Merged PR #1 (`faebb25`) | 2026-09-08 | Legacy specs referencing `backend/` | Single repo root convention for Go server. |
| **Backend Core** | Feature-based package modularization (`internal/<domain>/{repository,service,transport}`) | `ACCEPTED` | `api/internal/auth` implementation | 2026-09-08 | Legacy Clean Architecture spec | Reject deep layer-passing; prefer pragmatic domain encapsulation. |
| **Database** | PostgreSQL access via `pgx/v5` connection pooling and `sqlc` query generation | `ACCEPTED` | `api/go.mod`, `api/sqlc.yaml`, `api/pkg/util/database.go` | 2026-09-08 | Legacy GORM spec | Raw SQL performance, type-safe Go code generation, zero ORM magic. |
| **Database** | Database schema migrations use `golang-migrate` standard SQL scripts (`.up.sql`, `.down.sql`) | `ACCEPTED` | `api/migration/000001_init.up.sql` | 2026-09-08 | Legacy Goose migration spec | Numbered versioned SQL scripts. |
| **Backend API** | Shared structured application errors via `pkg/apperror` with domain error codes | `ACCEPTED` | `api/pkg/apperror/apperr.go` | 2026-09-08 | Ad-hoc Go errors | Centralized error code mapping to HTTP status codes. |
| **Backend API** | Standardized JSON HTTP response envelope `{ success, data, error }` via `pkg/response` | `ACCEPTED` | `api/pkg/response/response.go` | 2026-09-08 | Plain Gin JSON responses | Consistent response envelope across all endpoints. |
| **Auth** | Stateless JWT authentication with access/refresh tokens in `pkg/token` | `ACCEPTED` | `api/pkg/token/token.go`, `api/internal/auth/service/login.go` | 2026-09-08 | - | Signed JWT with HMAC-SHA256, custom claims (`id`, `role`, `type`). |
| **Frontend Core** | Next.js 16 (App Router), React 19, TypeScript, Bun package manager | `ACCEPTED` | `frontend/package.json`, `bun.lock` | 2026-09-08 | - | Standardized modern React stack with Bun runtime. |
| **Frontend UI** | Tailwind CSS v4, shadcn/ui components, Lucide React icons | `ACCEPTED` | `frontend/package.json`, `components.json` | 2026-09-08 | - | Unified accessible design system. |
| **Frontend State** | TanStack Query v5 for server state, Zustand v5 for client state, React Hook Form + Zod for forms | `ACCEPTED` | `frontend/package.json`, `frontend/src/providers/` | 2026-09-08 | - | Type-safe form validation and predictable caching. |
| **Frontend API** | Custom typed fetch transport (`createApiTransport`) with Zod decoders | `ACCEPTED` | `frontend/src/lib/api/transport.ts` | 2026-09-08 | Axios client assumption | Replaced third-party Axios with lightweight native fetch wrapper. |
| **Product Brand** | Official platform branding designated as "RoleCue" | `ACCEPTED` | `frontend/design/DESIGN-CONTRACT.md`, Brand artifacts | 2026-09-08 | Generic capstone title | Cohesive design identity, tokens, and logo assets established. |
| **JD Domain** | Separation of PDF file ingestion into raw text vs. structured LLM extraction | `ACCEPTED` | Jira task boundary: [[KAN-44]] vs. [[KAN-18]] | 2026-09-11 | Monolithic PDF-to-LLM prompt | Keeps PDF text extraction modular, testable, and interchangeable. |
| **JD Domain** | Formal JSON schema for Interview Blueprint | `PROPOSED` | Local Working Contract [[KAN-46]] (BR-01..BR-13) | 2026-09-11 | - | Assessment plan contract awaiting backend team review. |
| **Database** | Normalized `interview_blueprints` table (1:N from JD) & session re-parenting | `PROPOSED` | Local Working Contract [[KAN-46]], `Target-Database-ERD.drawio` | 2026-09-11 | Embedded `job_descriptions.blueprint` in PR #7 | First-class blueprint table; removes redundant session columns; adds immutable snapshot. |
| **Database** | Blueprint deletion protection via `ON DELETE RESTRICT` on `interview_sessions` | `PROPOSED` | Local Working Contract [[KAN-46]], `Target-Database-ERD.drawio` | 2026-09-11 | Cascade deletion assumption | Preserves historical sessions, turns, and performance reports when reusable blueprint is deleted. |
| **Interview Engine**| Adaptive runtime question generation vs. static pre-baked question list | `PROPOSED` | Local Working Contract [[KAN-46]] (BR-04, BR-05) | 2026-09-11 | - | Blueprint defines assessment objectives/budget; questions generated dynamically. |
| **JD Domain** | LLM Provider & Model for JD Extraction | `OPEN` | Candidates: OpenAI GPT-4o, Google Gemini 1.5/2.0, Claude 3.5 Sonnet | 2026-09-11 | Legacy spec mentions multi-provider | Must evaluate structured output latency, cost, and reliability. |
| **JD Domain** | Go PDF Extraction Library | `OPEN` | Candidates: `rsc/pdf`, `pdfcpu`, `ledongthuc/pdf`, CLI `pdftotext` | 2026-09-11 | - | Needs evaluation in [[KAN-44]]. |
| **Avatar / 3D** | Production 3D avatar rendering & blend-shape lip-sync architecture | `SPIKE` | Prototype in `@react-three/fiber`, Three.js | 2026-09-08 | - | Real-time GLTF morph target synchronization under test. |
| **Audio / Speech** | Speech-to-Text (STT) and Text-to-Speech (TTS) engine selection | `OPEN` | Candidates: Whisper / Deepgram (STT); ElevenLabs / Azure Speech (TTS) | 2026-09-11 | - | Requires latency benchmarking for sub-second conversational flow. |
| **Interview Engine**| Real-Time communication protocol (WebSocket vs. WebRTC) & state machine | `PROPOSED` | Legacy FSM in `IMPLEMENTATION_PLAN.md` | 2026-09-11 | - | Needs formal team ADR ratification before backend implementation. |
| **Payment** | Payment gateway provider | `OPEN` | Candidates: VNPay, MoMo, Stripe, PayOS | 2026-09-11 | Mentioned in Capstone Register | Academic requirement specifies Vietnamese gateway support. |
