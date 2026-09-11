---
project: SEP490
type: domain
status: draft
authority: team
last_verified: 2026-09-11
---

# JD Persistence & Database Layer

> **Tracking:** [[KAN-19]]  
> **Committed Deadline:** 2026-09-13 23:59  
> **Status:** `QUEUED`

---

## 1. Proposed Relational Model (PostgreSQL Target Architecture)

The target persistence layer separates the Job Description from the Interview Blueprint and re-parents Interview Sessions:

```sql
-- Job Descriptions (what the job requires; reviewed by candidate)
CREATE TABLE IF NOT EXISTS job_descriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    domain_id UUID REFERENCES technical_domains(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    raw_content TEXT,
    seniority VARCHAR(50),
    is_reviewed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Interview Blueprints (materialized assessment plans; 1 JD : N Blueprints)
CREATE TABLE IF NOT EXISTS interview_blueprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    jd_id UUID NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    duration_minutes INT NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    blueprint_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    version INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Interview Sessions (execution attempts; 1 Blueprint : N Sessions)
CREATE TABLE IF NOT EXISTS interview_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_id UUID NOT NULL REFERENCES interview_blueprints(id) ON DELETE RESTRICT,
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    avatar_id UUID NOT NULL REFERENCES avatar_profiles(id) ON DELETE RESTRICT,
    status session_status NOT NULL DEFAULT 'scheduled',
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    blueprint_snapshot JSONB NOT NULL,
    video_url VARCHAR(255),
    audio_url VARCHAR(255)
);

CREATE INDEX idx_job_descriptions_account_id ON job_descriptions(account_id);
CREATE INDEX idx_interview_blueprints_jd_id ON interview_blueprints(jd_id);
CREATE INDEX idx_interview_blueprints_account_id ON interview_blueprints(account_id);
CREATE INDEX idx_interview_sessions_blueprint_id ON interview_sessions(blueprint_id);
CREATE INDEX idx_interview_sessions_account_id ON interview_sessions(account_id);
```

---

## 2. Invariants & Business Rules (Proposed Team Contract)
- **1:N Cardinality (JD to Blueprints):** A JD belongs to an account and can have multiple associated `interview_blueprints` (BR-01).
- **1:N Cardinality (Blueprint to Sessions):** A candidate can attempt multiple `interview_sessions` against the same Blueprint (BR-02).
- **Decoupled from Embedded Columns:** Blueprints are not stored as an embedded column in `job_descriptions` (revising PR #7's `job_descriptions.blueprint jsonb`).
- **Session Authority Normalization:** `interview_sessions` drops redundant authority fields (`jd_id`, `difficulty`, `duration_minutes`, `total_questions`), deriving them from `interview_blueprints`.
- **Tamper-proof Session Snapshot:** `interview_sessions.blueprint_snapshot JSONB NOT NULL` freezes the full blueprint at session start so scoring and reports remain permanently reproducible.
- **Deletion Protection (`ON DELETE RESTRICT`):** `interview_sessions.blueprint_id` enforces `ON DELETE RESTRICT` (not `CASCADE`). Deleting a reusable Blueprint must never cascade-delete historical interview sessions, turns, or performance reports.
- **Compiled SQL:** All queries are generated via `sqlc` to `pgx/v5` structs.

---

## 3. Architectural Diagrams
- **Target Schema ERD (10 tables):** [Target-Database-ERD.drawio](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.drawio) | [Target-Database-ERD.md](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.md)
- **PR #7 Baseline ERD (9 tables):** [PR7-Database-ERD.drawio](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/pr7-database/PR7-Database-ERD.drawio) | [PR7-Database-ERD.md](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/pr7-database/PR7-Database-ERD.md)
