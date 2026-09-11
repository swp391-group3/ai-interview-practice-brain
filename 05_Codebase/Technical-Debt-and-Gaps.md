---
project: SEP490
type: code-reality
status: current
authority: local-brain
last_verified: 2026-09-11
---

# Technical Debt, Gaps & Identified Discrepancies

> [!WARNING]
> This document tracks confirmed contradictions between specifications, Jira tickets, and the current codebase.

---

## 1. Active Discrepancies

### Gap 1: Nested Login Route Path
- **Where:** `api/internal/auth/transport/http/server.go` (line 26)
- **Desired State:** Route accessible at `/auth/login` or `/api/v1/auth/login`.
- **Implementation Reality:** `r.Group("/auth")` registers `auth.POST("/auth/login", s.Login)`, resulting in `/auth/auth/login`.
- **Impact:** Frontend and external API callers fail with 404 if calling standard `/auth/login`.
- **Remediation:** Change handler registration to `auth.POST("/login", s.Login)`.

### Gap 2: Role ENUM Mismatch
- **Where:** `api/migration/000001_init.up.sql`
- **Desired State:** Roles are `Candidate` and `Admin` (as defined in Capstone Register and Specification).
- **Implementation Reality:** SQL ENUM defined as `participant`, `jury`, `admin`.
- **Impact:** Mismatch in JWT claims and authorization middleware.
- **Remediation:** Create migration `000002_fix_roles.up.sql` to align enum or map in Go adapter.

### Gap 3: sqlc Multi-Package Scope
- **Where:** `api/sqlc.yaml`
- **Current Reality:** Only compiles queries for `internal/auth/repository`.
- **Gap:** When JD queries are introduced in [[KAN-19]], `sqlc.yaml` must be updated to compile `internal/jd/repository/query/` or a unified query package.

### Gap 4: Transport Library Spec vs Reality
- **Where:** Old specs & frontend docs mention Axios.
- **Implementation Reality:** Code strictly uses custom native fetch transport `createApiTransport`.
- **Resolution:** Axios dropped; fetch transport ratified in [[Frontend-Contract]].
