---
project: SEP490
type: code-reality
status: current
authority: local-brain
last_verified: 2026-09-18
---

# Technical Debt, Gaps & Discrepancies

1. **Jira vs merge state:** KAN-19 is Done in Jira while its main repository/API work is PR #15 and remains open. Treat it as desired/delivery state, not merged code.
2. **Blueprint scope gap:** PR #15 creates `interview_blueprints` and removes embedded JD blueprint data, but does not re-parent sessions or implement the full target ERD/BR-01..BR-13.
3. **Role vocabulary:** database enum remains `participant`, `jury`, `admin`; product language differs.
4. **PDF/evaluation work:** KAN-44 and KAN-45 are in progress with no verified code decision in `main`.
5. **Tooling merge gap:** PR #14's Swagger/Testcontainers/lifecycle foundation is working-branch evidence only.

Resolved historical gaps: the nested login path is fixed; the JD domain and LLM integration do exist; the working PR resolves sqlc multi-package layout pending merge.
