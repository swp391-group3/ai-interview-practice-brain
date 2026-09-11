---
project: SEP490
type: execution
status: open
authority: jira
last_verified: 2026-09-12
---

# KAN-45: [Testing][JD] Set up JD Extraction Evaluation Dataset

## 1. Metadata
- **Key:** `KAN-45`
- **Component:** Testing / Quality Assurance
- **Committed Deadline:** **2026-09-12 23:59**
- **Status:** `QUEUED`

## 2. Goal & Intent
Create a curated, reusable benchmark dataset of 15-20 diverse Job Descriptions with human-verified ground-truth extraction targets to evaluate and regression-test the LLM pipeline.

## 3. Acceptance Criteria
- [ ] 15–20 real-world JD samples collected across multiple software engineering disciplines (Backend, Frontend, Fullstack, DevOps, Mobile).
- [ ] Ground-truth JSON files detailing expected skills, seniority, and core tech stacks.
- [ ] Reusable test runner script measuring Precision and Recall.

## 4. Open Questions / Missing Decisions
- Storage location: committed in repository under `api/testdata/` or external object storage? `[NEEDS TEAM DECISION]`
