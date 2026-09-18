---
project: SEP490
type: code-reality
status: current
authority: local-brain
last_verified: 2026-09-18
---

# Technical Debt, Gaps & Discrepancies

1. **Resolved Jira vs merge state:** KAN-19 Done now aligns with merged PR #15; the earlier mismatch remains historical Sync Log evidence only.
2. **Blueprint scope gap:** merged PR #15 creates `interview_blueprints` and removes embedded JD blueprint data, but does not re-parent sessions or implement the full target ERD/BR-01..BR-13.
3. **Role vocabulary:** database enum remains `participant`, `jury`, `admin`; product language differs.
4. **PDF/evaluation work:** KAN-44 and KAN-45 are in progress with no verified code decision in `main`.
5. **Tooling baseline:** PR #14's Swagger/Testcontainers/lifecycle foundation is merged; only later tooling changes need separate verification.

Resolved historical gaps: the nested login path is fixed; JD extraction, persistence/API, and feature-local sqlc all exist in merged code.
