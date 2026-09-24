---
title: Data Relationships and Invariants
tags:
  - system
  - data-model
  - cardinalities
  - invariants
  - integrity
aliases:
  - Data Relationships
  - Entity Cardinalities
---

# Data Relationships & Cardinality Invariants

This document specifies the conceptual entity relationships, cardinalities, cascade behaviors, and lifecycle invariants governing data integrity across RoleCue.

---

## 1. Master Relationship Cardinality Matrix

| Parent Entity | Child Entity | Cardinality | Nullable FK? | Cascade Policy | Business Rationale |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **`UserAccount`** | `CandidateProfile` | `1 : 0..1` | No | `CASCADE` | Unique candidate profile record per candidate account. |
| **`UserAccount`** | `RecruiterProfile` | `1 : 0..1` | No | `CASCADE` | Unique recruiter employer profile per recruiter account. |
| **`UserAccount`** | `CreditAccount` | `1 : 1` | No | `RESTRICT` | Financial balance record created on registration. |
| **`UserAccount`** | `PaymentTransaction` | `1 : 0..*` | No | `RESTRICT` | Financial ledger must never be accidentally deleted. |
| **`PaymentTransaction`** | `RefundRequest` | `1 : 0..1` | No | `RESTRICT` | At most one dispute per payment transaction. |
| **`UserAccount`** | `TargetJD` | `1 : 0..*` | No | `CASCADE` | Candidate owns zero or more practice target JDs. |
| **`TargetJD`** | `InterviewBlueprint` | `1 : 0..*` | No | `CASCADE` | One reviewed JD can generate multiple blueprints across difficulties. |
| **`InterviewBlueprint`** | `InterviewSession` | `1 : 0..*` | No | `RESTRICT` | **CRITICAL:** Reusable blueprint can launch multiple sessions. Deleting blueprint must **NEVER** delete historical sessions. |
| **`InterviewSession`** | `SessionTurn` | `1 : 0..*` | No | `CASCADE` | Sequential conversational dialogue turns in a session. |
| **`InterviewSession`** | `PerformanceReport` | `1 : 0..1` | No (Unique) | `CASCADE` | Strictly at most one final report per session. |
| **`UserAccount`** | `JobPosting` | `1 : 0..*` | No | `RESTRICT` | Recruiter authors zero or more company Job Postings. |
| **`JobPosting`** | `Application` | `1 : 0..*` | No | `RESTRICT` | Candidate applications submitted to an active Job Posting. |
| **`UserAccount`** | `Application` | `1 : 0..*` | No | `RESTRICT` | Candidate submits zero or more applications. |
| **`UserAccount`** | `PersonalAvatar` | `1 : 0..*` | No | `CASCADE` | Candidate owns personal 3D avatars generated from photos. |
| **`VoiceProfile`** | `InterviewSession` | `1 : 0..*` | Yes | `SET NULL` | Voice persona used by session; deleting profile resets session to default. |

---

## 2. Core Integrity Invariants

### 2.1. Historical Session Immutability
```mermaid
flowchart LR
    BP["Interview Blueprint (Reusable)"] -->|"Instantiates"| SESS["Interview Session"]
    SESS -->|"Stores At Creation"| SNAP["blueprint_snapshot JSONB NOT NULL"]
    SNAP -->|"Immutable Reference"| REP["Performance Report"]
```
* **Invariant:** Every `InterviewSession` must persist an immutable `blueprint_snapshot JSONB NOT NULL` at the moment of session creation.
* **Integrity Guarantee:** Even if the parent `TargetJD` is modified, the `InterviewBlueprint` is regenerated, or system-wide rubrics are updated, historical evaluation reports and turn scores remain 100% reproducible and immune to retrospective distortion.

### 2.2. Blueprint Preservation via `ON DELETE RESTRICT`
* **Invariant:** The foreign key constraint between `InterviewSession` and `InterviewBlueprint` must use `ON DELETE RESTRICT`.
* **Integrity Guarantee:** If a user attempts to delete a saved Interview Blueprint from their library, the deletion must be rejected if completed interview sessions reference it. Historical practice records and transcripts must never be orphaned or deleted via cascade.

### 2.3. Single Performance Report per Session
* **Invariant:** `PerformanceReport` enforces a strict `UNIQUE(session_id)` constraint.
* **Integrity Guarantee:** A completed interview session produces exactly one authoritative evaluation report. Re-submitting evaluation triggers cannot duplicate reports.

### 2.4. Independent Relational Tenancy
* **Invariant:** RoleCue does not use multi-tenant schemas or Row-Level Security tenant isolation policies.
* **Integrity Guarantee:**
  * Recruiter data is partitioned relationally by `recruiter_id`.
  * Company details exist as profile attributes attached to the recruiter, not an architectural tenant boundary.
  * Candidate data is strictly isolated relationally by `candidate_id` / `user_id`.

### 2.5. ACID Transactional Ledger for Balances
* **Invariant:** All updates to `CreditAccount.balance` must occur within explicit database transactions (`BEGIN ... COMMIT`) utilizing row-level locks (`SELECT ... FOR UPDATE`).
* **Integrity Guarantee:** Prevents double-spend concurrency anomalies when launching sessions or processing concurrent payment webhooks.
