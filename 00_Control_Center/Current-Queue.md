---
project: SEP490
type: execution
status: current
authority: jira
last_verified: 2026-09-18
---

# Current Execution Queue

| Jira | Current Jira status | Code / delivery reading |
|---|---|---|
| [[KAN-18]] | `DONE` | Merged structured JD extraction |
| [[KAN-19]] | `DONE` | Merged reviewed-JD persistence and authenticated REST API (PR #15) |
| [[KAN-46]] | `DONE` | Contract/design completed; full database/session realization is not proven |
| [[KAN-20]] | `IN PROGRESS` | JD upload/review/preview UI; code remains placeholder at last verification |
| [[KAN-44]] | `IN PROGRESS` | PDF extraction; library choice not verified |
| [[KAN-45]] | `IN PROGRESS` | Extraction evaluation dataset |
| KAN-76 | `IN PROGRESS` | Report 1 |
| KAN-41 | `IN PROGRESS` | Backend/frontend/E2E test infrastructure |
| KAN-34 | `IN PROGRESS` | Frontend login/password sign-in |
| KAN-47 | `IN PROGRESS` | Public landing page |
| KAN-27 | `DONE` | UI/UX direction/design system |
| KAN-10 | `DONE` | Next.js foundation |

The 2026-09-11–14 JD sprint is historical, not a current deadline table. Dependencies remain: extraction informs persistence; persistence/API informs UI; PDF ingestion is intentionally independent from LLM extraction.
