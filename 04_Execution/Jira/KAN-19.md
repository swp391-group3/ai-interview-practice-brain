---
project: SEP490
type: execution
status: done
authority: jira
last_verified: 2026-09-18
---

# KAN-19: JD Repository, Use Cases and REST Endpoints

**Jira:** `DONE`.

**OPEN PR / WORKING IMPLEMENTATION:** PR #15 (`feature/jd-api`) supplies PostgreSQL/sqlc persistence, ownership-scoped CRUD, six authenticated `/jds` routes, response/error mappings, multi-entry sqlc config, and the blueprint migration.

**GAP / authority discrepancy:** PR #15 is still open and unmerged, so none of that is merged `main` implementation. Old `/api/v1/jd/*` routes are superseded. See [[JD-Persistence]] and [[API-Contract]].
