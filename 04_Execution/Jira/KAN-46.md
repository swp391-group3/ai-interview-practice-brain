---
project: SEP490
type: execution
status: draft
authority: jira
last_verified: 2026-09-11
---

# KAN-46: [Backend][JD] Define JD Interview Blueprint Contract

## 1. Metadata
- **Key:** `KAN-46`
- **Component:** Backend / JD Domain
- **Committed Deadline:** **2026-09-11 14:00**
- **Status:** `IN PROGRESS`

## 2. Goal & Intent
Stabilize the contract and JSON schema for the **Interview Blueprint**. The blueprint is the output of the JD analysis process and the input contract for the downstream real-time interview orchestrator.

## 3. Acceptance Criteria
- [ ] Define JSON schema for the interview blueprint specifying:
  - Estimated duration and stage breakdown (e.g., introduction, technical deep dive, behavioral/system design, wrap-up).
  - Question budget per stage.
  - Target skills and evaluation competencies to assess.
  - Difficulty rating (Junior, Mid, Senior, Lead).
- [ ] Contract is reviewed and ratified by backend and frontend leads.
- [ ] Documented in [[JD-Blueprint]] and [[JD-Contract]].

## 4. Open Questions / Missing Decisions
- Should question seed topics be generated during blueprint creation or dynamically during the interview turn-taking? `[NEEDS TEAM DECISION]`
