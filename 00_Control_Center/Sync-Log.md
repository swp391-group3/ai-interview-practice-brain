---
project: SEP490
type: control
status: current
authority: local-brain
last_verified: 2026-09-11
---

# Vault Synchronization Log

> [!NOTE]
> This log records operational and architectural deltas between the local project brain, team decisions, repository changes, and external AI tools (ChatGPT/Claude). Log entries record **deltas only**, not redundant copies.

---

## 2026-09-11 10:00

**Source:** Local Vault Migration & Codebase Inspection  
**Trigger:** Full migration of SEP490 Obsidian vault into an operational project brain.

### Changed
- Vault restructured into standardized operational directories: `00_Control_Center/`, `01_Contracts/`, `02_Decisions/`, `03_Domains/`, `04_Execution/`, `05_Codebase/`, `06_Meetings/`, `07_Research-Spikes/`, `08_Reports/`, `90_Legacy-Reference/`, `99_Inbox/`.
- Legacy `SPECIFICATION.md` and `IMPLEMENTATION_PLAN.md` moved to `90_Legacy-Reference/` with prominent non-normative warnings.
- Academic submission templates and lecturer guidance moved to `08_Reports/`.

### Decision Updates
- **Backend Root:** Verified at `api/` (superseding legacy `backend/` references).
- **Backend Architecture:** Feature-based modular structure confirmed (`internal/auth/`, `pkg/apperror`, `pkg/response`). Clean Architecture rejected.
- **Database Access:** `pgx/v5` connection pool + `sqlc` code generation confirmed. GORM rejected.
- **Migrations:** `golang-migrate` standard SQL scripts (`000001_init.up.sql`) confirmed. Goose rejected.
- **Frontend Stack:** Next.js 16 (App Router), React 19, Bun, Tailwind CSS v4, shadcn/ui confirmed.
- **Product Name:** "RoleCue" confirmed as formal design brand identity.

### Contracts Affected
- Created initial draft contracts in `01_Contracts/`: Product, Backend, Frontend, API, JD, Interview, Avatar-Audio, Payment.

### Jira Affected
- Cataloged active JD sprint tickets: [[KAN-46]], [[KAN-18]], [[KAN-44]], [[KAN-45]], [[KAN-19]], [[KAN-20]].

### Code Reality Affected
- Audited `api/` and `frontend/` repositories. Confirmed that JD domain does not exist in code yet.
- Noted discrepancy in backend login route: `/auth/auth/login`.
- Noted database role enum discrepancy: `participant`, `jury`, `admin` vs. `Candidate` and `Admin`.

### Open Questions Cataloged
- OQ-01: Blueprint JSON schema contract ([[KAN-46]]).
- OQ-02: Structured JD extraction schema ([[KAN-18]]).
- OQ-03: PDF text extraction library selection ([[KAN-44]]).
- OQ-04: sqlc multi-package configuration strategy.
- OQ-05 to OQ-09: LLM provider, 3D avatar rendering pipeline, STT/TTS engines, Payment provider, Account roles.
