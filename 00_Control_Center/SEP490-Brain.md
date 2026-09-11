---
project: SEP490
type: control
status: current
authority: local-brain
last_verified: 2026-09-11
---

# SEP490 Project Brain — Command Center

> **Operational Hub & Navigation Center**  
> **Product:** RoleCue — AI-Powered Virtual Technical Mock Interview Platform  
> **Capstone Group:** 09 (`09_GFA26SE84`) | **Supervisor:** Mr. Nguyễn Thế Hoàng  
> **Current Date:** 2026-09-11 | **Active Sprint Focus:** Job Description (JD) Processing Pipeline

---

## ⚡ Quick Navigation

| Operational Zone | Key Notes & Maps | Primary Role / Description |
| :--- | :--- | :--- |
| **Control Center** | [[Source-of-Truth]]<br>[[Decision-Registry]]<br>[[Open-Questions]]<br>[[Current-State]]<br>[[Current-Queue]]<br>[[Sync-Log]] | Normative authority rules, accepted architectural records, open blockers, active queues, sync deltas. |
| **System Contracts** | [[Product-Contract]]<br>[[Backend-Contract]]<br>[[Frontend-Contract]]<br>[[API-Contract]]<br>[[JD-Contract]]<br>[[Interview-Contract]]<br>[[Avatar-Audio-Contract]]<br>[[Payment-Contract]] | Authoritative behavior, inputs/outputs, invariants, and boundaries for all subsystems. |
| **Feature Domains** | [[JD-Overview]]<br>[[03_Domains/Auth/README\|Auth Domain]]<br>[[03_Domains/Interview/README\|Interview Domain]]<br>[[03_Domains/Avatar-Audio/README\|Avatar & Audio]]<br>[[03_Domains/Evaluation-Reporting/README\|Evaluation Domain]]<br>[[03_Domains/Payment/README\|Payment Domain]]<br>[[03_Domains/Admin/README\|Admin Domain]] | Deep domain logic, workflows, specifications, and specialized schemas. |
| **Codebase Reality** | [[Repo-Map]]<br>[[Backend-Reality]]<br>[[Frontend-Reality]]<br>[[Integration-Boundaries]]<br>[[Technical-Debt-and-Gaps]] | Ground-truth audit of merged code in `api/` and `frontend/`. Identifies gaps vs. specs. |
| **Execution & Jira** | [[Current-Sprint]]<br>[[Dependency-Map]]<br>[[Done-History]]<br>[[KAN-46]] · [[KAN-18]] · [[KAN-44]] · [[KAN-45]] · [[KAN-19]] · [[KAN-20]] | Sprint tracking, Jira task dependencies, deadlines, and execution order. |
| **Academic Reports** | [[08_Reports/README\|Reports Hub]]<br>[[08_Reports/Lecturer/Lecturer-note.jpg\|Lecturer Directives]]<br>[[08_Reports/Lecturer/9_GFA26SE84_AI_Virtual_Technical_Interview_Capstone_Register.pdf\|Capstone Register]] | University deliverables, submission templates, supervisor constraints. |
| **Historical Archive** | [[90_Legacy-Reference/README\|Legacy Reference Hub]]<br>[[SPECIFICATION]]<br>[[IMPLEMENTATION_PLAN]] | Speculative, unapproved, or superseded historical artifacts (*Reference only*). |

---

## 🎯 Current Operational Focus: JD Domain Sprint

The active execution stream focuses on stabilizing the **Job Description (JD) extraction and blueprinting pipeline**:

```mermaid
flowchart LR
    K46["KAN-46: Blueprint Contract<br/>(Due: 09-11 14:00)"] --> K18["KAN-18: JD Extraction & Domain<br/>(Due: 09-11 23:59)"]
    K18 --> K45["KAN-45: Evaluation Dataset<br/>(Due: 09-12 23:59)"]
    K18 --> K44["KAN-44: PDF Ingestion<br/>(Due: 09-12 18:00)"]
    K18 --> K19["KAN-19: Endpoints & Repo<br/>(Due: 09-13 23:59)"]
    K19 --> K20["KAN-20: Review & Preview UI<br/>(Due: 09-14 23:59)"]
```

- **Active Blocker / Task:** Stabilize [[KAN-46]] contract and proceed directly to [[KAN-18]].
- **Open Decisions to Resolve:** See [[Open-Questions]] for LLM provider choice, PDF parsing library, and schema design.
