---
project: SEP490
type: domain
status: working
authority: open-pr
last_verified: 2026-09-18
---

# JD Persistence

## OPEN PR / WORKING IMPLEMENTATION — PR #15

PR #15 uses a PostgreSQL/sqlc feature repository and authenticated ownership-scoped Create/List/Get/Update/Delete operations. `Analyze` is separate and never saves. `Create` preserves `rawText`, requires a reviewed structured JD with explicit seniority, and writes `customized`; `Update` changes reviewed structured data but not raw text. Ownership is in SQL, so another user's resource appears not found.

Current field concepts: `user_id`, `title`, `seniority_level`, `raw_text`, `parsed_data`, `status`. The starting migration also contains legacy `job_description_skills`; PR #15 persists reviewed competency collections in `parsed_data`. Do not report `account_id`, `is_reviewed`, or `raw_content` as implementation fields.

The PR is open despite Jira KAN-19 `DONE`; this is a documented authority discrepancy. Routes and response details live in [[API-Contract]].
