---
project: SEP490
type: execution
status: open
authority: jira
last_verified: 2026-09-11
---

# KAN-19: Implement JD Repository, Use Cases and REST Endpoints

## 1. Metadata
- **Key:** `KAN-19`
- **Component:** Backend / Database & HTTP Transport
- **Committed Deadline:** **2026-09-13 23:59**
- **Status:** `QUEUED` (Depends on [[KAN-18]])

## 2. Goal & Intent
Implement the PostgreSQL database schema for storing Job Descriptions and Blueprints, compile type-safe queries via `sqlc`, and expose REST HTTP handlers wrapped in `pkg/response`.

## 3. Acceptance Criteria
- [ ] Migration script `000002_create_jd_tables.up.sql` created in `api/migration/`.
- [ ] `sqlc` queries compiled to Go repository structs.
- [ ] HTTP handlers implemented in `api/internal/jd/transport/http/`.
- [ ] Endpoints mounted on Gin router:
  - `POST /api/v1/jd/upload`
  - `GET /api/v1/jd/:id`
  - `PUT /api/v1/jd/:id`
  - `POST /api/v1/jd/:id/blueprint`
- [ ] Endpoints return standardized envelope `{ success, data, error }`.

## 4. Open Questions / Missing Decisions
- sqlc package configuration for JD domain (see [[Open-Questions]] OQ-04).
