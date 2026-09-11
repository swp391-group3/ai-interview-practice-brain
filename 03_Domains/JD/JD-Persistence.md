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

## 1. Proposed Relational Model (PostgreSQL)

```sql
CREATE TABLE IF NOT EXISTS job_descriptions (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    title text NOT NULL,
    raw_content text NOT NULL,
    source_type text NOT NULL DEFAULT text, -- text or pdf
    seniority text,
    extracted_data jsonb NOT NULL DEFAULT {}::jsonb,
    is_reviewed boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS interview_blueprints (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    jd_id uuid NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
    blueprint_data jsonb NOT NULL DEFAULT {}::jsonb,
    version int NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_job_descriptions_account_id ON job_descriptions(account_id);
CREATE INDEX idx_interview_blueprints_jd_id ON interview_blueprints(jd_id);
```

---

## 2. Invariants
- A JD belongs to exactly one candidate account.
- Extracted skills and parameters are stored in `extracted_data` (JSONB) for flexible queryability.
- Blueprints are versioned and linked to their originating JD.
- All database queries must be compiled via `sqlc` to `pgx/v5` structs.
