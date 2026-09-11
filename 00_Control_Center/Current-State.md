---
project: SEP490
type: control
status: current
authority: local-brain
last_verified: 2026-09-11
---

# Current Project State

> **Snapshot Date:** 2026-09-11  
> **Phase:** Capstone Development — Phase 1: JD Ingestion & Analysis Pipeline  
> **Repository:** \`github.com/swp391-group3/ai-interview-practice\`

---

## 1. System Implementation Baseline

### Backend (\`api/\`)
- **Language & Runtime:** Go 1.27, Gin Web Framework.
- **Data Layer:** PostgreSQL with \`jackc/pgx/v5\` connection pool and \`sqlc\` query compiler.
- **Migrations:** \`api/migration/000001_init.up.sql\` executed (creates \`accounts\` table with roles \`participant\`, \`jury\`, \`admin\`).
- **Implemented Packages:**
  - \`api/internal/auth/\`: Login authentication, JWT generation, password verification.
  - \`api/internal/shared/\`: Environment config parsing and HTTP server assembly.
  - \`api/pkg/apperror/\`: Structured domain error codes.
  - \`api/pkg/response/\`: Standardized JSON envelope (\`success\`, \`data\`, \`error\`).
  - \`api/pkg/token/\`: JWT access/refresh token signing and verification.
  - \`api/pkg/util/\`: Database pool initialization.
- **JD Domain Reality:** \`api/internal/jd/\` **does not exist yet**. All JD functionality is currently in execution queue.

### Frontend (\`frontend/\`)
- **Framework & Runtime:** Next.js 16 (App Router), React 19, TypeScript, Bun package manager.
- **Styling & UI:** Tailwind CSS v4, shadcn/ui components, Lucide icons.
- **Data & Transport:** Custom typed fetch transport (\`createApiTransport\`), TanStack Query v5, Zustand v5.
- **Forms & Validation:** React Hook Form, Zod v4.
- **Current Routes:** Skeleton shell present for \`/(candidate)\`, \`/admin\`, \`/(public)\`.
- **JD Feature State:** \`frontend/src/features/job-description\` contains only a placeholder component (\`RoutePlaceholder\`).

---

## 2. In-Flight Execution Focus

The team is actively executing the **Job Description (JD) processing pipeline**:
- **Immediate milestone:** Ratify the Interview Blueprint contract ([[KAN-46]]) by 14:00 today.
- **Core implementation:** Build structured JD extraction domain model and LLM integration ([[KAN-18]]) by 23:59 today.
- **Subsequent steps:** Pipeline uncoupling of PDF ingestion ([[KAN-44]]), evaluation dataset curation ([[KAN-45]]), REST API endpoints ([[KAN-19]]), and Candidate UI ([[KAN-20]]).

See [[Current-Queue]] and [[Current-Sprint]] for detailed timeline and execution order.

---

## 3. Discrepancies & Known Gaps (Implementation Reality vs. Spec)

1. **Backend Route Path Typo:** In \`api/internal/auth/transport/http/server.go\`, route is registered as \`auth.POST("/auth/login", s.Login)\` inside group \`/auth\`, resulting in actual HTTP path \`/auth/auth/login\`.
2. **Account Role ENUM Mismatch:** Database migration has \`participant\`, \`jury\`, \`admin\`. Capstone specification defines \`Candidate\` and \`Admin\`.
3. **sqlc Scoping:** Currently only configured for \`internal/auth/repository\`. Needs multi-package configuration for future domains.
4. **Transport Layer:** Spec mentions Axios; actual frontend code implements custom fetch wrapper (\`frontend/src/lib/api/transport.ts\`).
