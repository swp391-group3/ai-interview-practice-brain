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

## 3. Working Consensus & Proposed Team Contract (BR-01 to BR-13)

> [!NOTE]
> **Authority Notice:** These decisions represent our **Local Working Contract / Proposed Team Contract**. They have NOT been committed to Jira nor merged into PR #7. They remain `PROPOSED` pending backend lead and team ratification.

- **BR-01 (1:N JD to Blueprint):** One Job Description can yield multiple Blueprints (different difficulty, duration, focus areas).
- **BR-02 (1:N Blueprint to Session):** One Blueprint can be practiced multiple times across separate interview sessions.
- **BR-03 (Prerequisite):** Blueprints require a candidate-reviewed JD (`is_reviewed = true`).
- **BR-04 (Assessment Plan Scope):** Blueprint specifies evaluation objectives, stages, timing, and question budgets. It does **NOT** pre-generate a static question list.
- **BR-05 (Dynamic Question Generation):** Concrete questions are adaptively generated at runtime during turns.
- **BR-06 (Dedicated Persistence):** First-class `interview_blueprints` table (decoupled from `job_descriptions.blueprint` column).
- **BR-07 (Session Re-parenting):** `interview_sessions` references `blueprint_id` (`interview_blueprints.id`).
- **BR-08 (Removal of Redundant Session Fields):** `jd_id`, `difficulty`, `duration_minutes`, `total_questions` removed from `interview_sessions`.
- **BR-09 (Session Immutability Snapshot):** `interview_sessions` contains `blueprint_snapshot JSONB NOT NULL` to preserve grading reproducibility.
- **BR-10 (Session Status Lifecycle):** Tracked via `session_status` enum (`scheduled`, `in_progress`, `completed`, `cancelled`).
- **BR-11 (Turn Granularity):** Recorded in `session_turns` with timestamps, audio/video text, duration, and turn evaluation.
- **BR-12 (Grading Report 1:1):** One `performance_reports` record per completed session.
- **BR-13 (Deletion Protection):** `interview_sessions.blueprint_id` uses `ON DELETE RESTRICT`. Deleting a reusable Blueprint must never cascade-delete historical sessions, turns, or performance reports.
- **Authority Rule:** Stored as local working contract; not marked team-wide `ACCEPTED` until ratified by backend team.

---

## 4. Acceptance Criteria Status

- [x] Define JSON schema for the interview blueprint specifying:
  - Estimated duration and stage breakdown (introduction, technical deep dive, behavioral, wrap-up).
  - Question budget per stage.
  - Target skills and evaluation competencies to assess.
  - Difficulty rating (`junior`, `middle`, `senior`, `lead`).
- [x] Target relational database model designed, validated, and rendered (`Target-Database-ERD.drawio` with `ON DELETE RESTRICT`).
- [x] Architecture diagrams designed and validated (Data Flow, Sequence, Lifecycle).
- [ ] Contract is reviewed and ratified by backend and frontend leads (pending sprint sync).
- [x] Documented in [[JD-Blueprint]] and [[JD-Contract]].

---

## 5. Architectural References
- **Target Schema ERD:** [Target-Database-ERD.drawio](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.drawio) | [Target-Database-ERD.png](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.png) | [Target-Database-ERD.md](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.md)
- **Data Flow Architecture:** [jd-to-blueprint-dataflow.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-dataflow/jd-to-blueprint-dataflow.html)
- **Sequence Architecture:** [generate-preview-save-execute-sequence.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-sequence/generate-preview-save-execute-sequence.html)
- **Lifecycle Architecture:** [interview-blueprint-lifecycle.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-lifecycle/interview-blueprint-lifecycle.html)
- **PR #7 Reproduction ERD:** [PR7-Database-ERD.drawio](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/pr7-database/PR7-Database-ERD.drawio) | [PR7-Database-ERD.md](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/pr7-database/PR7-Database-ERD.md)

---

## 6. Open Questions / Missing Decisions
- **Question Seed Generation:** Resolved locally in proposed contract (BR-04, BR-05: runtime adaptive generation); awaiting backend team ratification.
