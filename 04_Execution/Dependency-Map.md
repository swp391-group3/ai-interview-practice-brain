---
project: SEP490
type: execution
status: current
authority: jira
last_verified: 2026-09-11
---

# Subsystem & Task Dependency Map

## 1. Formal Jira Dependencies
- [[KAN-18]] (`JD Domain & Extraction`) -> [[KAN-19]] (`JD Repository & REST Endpoints`)
- [[KAN-19]] (`JD Repository & REST Endpoints`) -> [[KAN-20]] (`Candidate UI Review & Preview`)

## 2. Architectural Pre-requisites & Decoupling
- **KAN-46 (Blueprint Contract) precedes KAN-18:** Ratifying the blueprint output shape ensures that the LLM extraction in KAN-18 accurately supplies the needed fields.
- **KAN-44 (PDF Ingestion) is decoupled from KAN-18:** PDF parsing converts binary files to UTF-8 text. It does not depend on LLM logic, enabling independent parallel development.
- **KAN-45 (Evaluation Dataset):** Consumes the schema defined in KAN-18 to establish automated benchmark tests.

## 3. Downstream Subsystem Dependencies
- **Interview Simulation Domain:** Depends on the persisted Blueprint produced by [[KAN-19]] / [[KAN-46]].
- **Evaluation & Reporting Domain:** Depends on the Blueprint rubric produced in [[KAN-46]].
