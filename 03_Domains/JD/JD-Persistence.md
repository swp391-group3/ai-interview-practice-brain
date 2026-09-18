---
project: SEP490
type: domain
status: current
authority: code
last_verified: 2026-09-18
---

# JD Persistence

## MERGED IMPLEMENTATION — PR #15

PR #15 uses a PostgreSQL/sqlc feature repository and authenticated ownership-scoped Create/List/Get/Update/Delete operations. `Analyze` is separate and never saves. `Create` preserves `rawText`, requires a reviewed structured JD with explicit seniority, and writes `customized`; `Update` changes reviewed structured data but not raw text. Ownership is in SQL, so another user's resource appears not found.

Current field concepts: `user_id`, `title`, `seniority_level`, `raw_text`, `parsed_data`, `status`. The starting migration also contains legacy `job_description_skills`; PR #15 persists reviewed competency collections in `parsed_data`. Do not report `account_id`, `is_reviewed`, or `raw_content` as implementation fields.

KAN-19 Jira `DONE` and the merged PR #15 implementation now align. List uses merged `limit`/`offset` pagination; routes and response details live in [[API-Contract]].
