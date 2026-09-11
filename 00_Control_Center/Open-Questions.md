---
project: SEP490
type: control
status: current
authority: team
last_verified: 2026-09-11
---

# Open Architecture & Product Questions

> [!IMPORTANT]
> Unresolved decisions must NOT be silently filled with arbitrary choices. Every unresolved architecture, product, or integration question is cataloged here until officially resolved by team consensus or an accepted ADR.

---

## 1. Active Blockers (Immediate Sprint Focus)

### OQ-01: Exact Interview Blueprint Schema Specification & Data Model
- **Area:** JD & Interview Interface / Database Architecture
- **Why it matters:** Defines the contract between JD analysis output, database persistence, and downstream real-time interview orchestrator.
- **Blocking:** [[KAN-46]] and [[KAN-18]] implementation.
- **Working Proposal (Local Working Decisions BR-01 to BR-13):**
  - **Cardinalities:** JD (1) -> (N) Blueprints; Blueprint (1) -> (N) Sessions.
  - **Separation of Concerns:** JD = Job requirements; Interview Config = Candidate session settings; Blueprint = Assessment plan (stages, duration, rubric, question budget); Runtime Questions = Adaptively generated at runtime during turns.
  - **Relational Model:** Normalized `interview_blueprints` table (extracted from `job_descriptions.blueprint`); `interview_sessions` re-parented to `blueprint_id` with `ON DELETE RESTRICT`; redundant session columns removed; immutable `blueprint_snapshot JSONB NOT NULL` preserved on sessions.
  - **Architecture Models:** Data Flow, Sequence, and Lifecycle state machines authored and validated via Archify showcase profile.
- **Owner:** Backend Lead / Team Consensus
- **Status:** `PROPOSED` (Local working contract formulated in [[KAN-46]], `Target-Database-ERD.drawio`, and Archify diagrams; awaiting backend team review & ratification)
- **Resolution Link:** [[JD-Blueprint]] | [[KAN-46]] | [Target-Database-ERD.md](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.md)

---

### OQ-02: Structured JD Extraction Schema & Skill Taxonomy
- **Area:** JD Domain
- **Why it matters:** Governs what the LLM extracts from raw JD text and what the candidate reviews and edits before starting an interview.
- **Blocking:** [[KAN-18]], [[KAN-20]].
- **Candidate Options:**
  - Flat skill list + seniority string + summary.
  - Hierarchical categories: Required Skills, Preferred Skills, Core Technologies, Domain Concepts, Seniority Level, Expected Years of Experience.
- **Owner:** Backend / Prompt Engineer
- **Status:** `OPEN`
- **Resolution Link:** Pending [[JD-Extraction]] / [[KAN-18]]

---

### OQ-03: Go PDF Text Extraction Library / Strategy
- **Area:** JD Ingestion
- **Why it matters:** Must reliably extract plain UTF-8 text from diverse multi-page PDF resumes/job postings without corrupting formatting.
- **Blocking:** [[KAN-44]] (Committed deadline: 2026-09-12 18:00).
- **Candidate Options:**
  - Pure Go library: `pdfcpu`, `github.com/ledongthuc/pdf`, or `rsc/pdf`.
  - System utility wrapper: `pdftotext` (poppler-utils) via `exec.Command`.
  - External dedicated microservice / container.
- **Owner:** Backend Developer
- **Status:** `OPEN`
- **Resolution Link:** Pending [[JD-PDF-Ingestion]] / [[KAN-44]]

---

### OQ-04: sqlc Layout and Multi-Domain Directory Strategy
- **Area:** Backend Database Architecture
- **Why it matters:** Currently `api/sqlc.yaml` only compiles `internal/auth/repository/query/` into `internal/auth/repository`. When JD queries are added, do we keep isolated repository packages per domain or a unified database query package?
- **Blocking:** [[KAN-19]] (Committed deadline: 2026-09-13 23:59).
- **Candidate Options:**
  - Option A: Multi-package sqlc (add entry in `sqlc.yaml` for `internal/jd/repository/query/` -> `internal/jd/repository`).
  - Option B: Centralized `api/internal/db/` or `api/internal/shared/db/` package.
- **Owner:** Backend Team
- **Status:** `OPEN`
- **Resolution Link:** Pending [[Backend-Contract]]

---

## 2. Upstream & Medium-Term Questions

### OQ-05: LLM Provider, Model Version, and Failover Strategy
- **Area:** AI Engine
- **Why it matters:** High impact on latency, API cost, Vietnamese/English tokenization quality, and structured JSON output adherence.
- **Candidate Options:**
  - OpenAI GPT-4o / GPT-4o-mini (structured JSON mode).
  - Google Gemini 1.5 Pro / Flash / 2.0.
  - Anthropic Claude 3.5 Sonnet.
- **Status:** `OPEN`
- **Resolution Link:** Unresolved

---

### OQ-06: Production 3D Avatar Rendering & Lip-Sync Pipeline
- **Area:** Avatar & Audio
- **Why it matters:** Real-time WebGL rendering must stay performant on modest student hardware (target 20 concurrent users, acceptable FPS) with natural viseme interpolation.
- **Candidate Options:**
  - `@react-three/fiber` + Ready Player Me GLB avatars + Rhubarb viseme mapping.
  - Pre-rendered 2D/video fallback for low-end devices.
- **Status:** `SPIKE` (Proof-of-concept exists in frontend dependencies; pipeline unratified)
- **Resolution Link:** Pending [[Avatar-Audio-Contract]]

---

### OQ-07: Speech-to-Text (STT) and Text-to-Speech (TTS) Stack
- **Area:** Avatar & Audio
- **Why it matters:** Conversational turn-taking requires round-trip latency < 1.5s to feel realistic.
- **Candidate Options:**
  - STT: Whisper API, Deepgram Nova-2, browser Web Speech API.
  - TTS: Azure Speech, ElevenLabs, OpenAI TTS.
- **Status:** `OPEN`
- **Resolution Link:** Unresolved

---

### OQ-08: Third-Party Payment Gateway Selection
- **Area:** Billing / Monetization
- **Why it matters:** Capstone registration requires payment integration supporting candidate subscription/credits.
- **Candidate Options:** PayOS, VNPay, MoMo, Stripe.
- **Status:** `OPEN`
- **Resolution Link:** Pending [[Payment-Contract]]

---

### OQ-09: Role Discrepancy in Database vs. Product Scope
- **Area:** Auth & Access Control
- **Why it matters:** `api/migration/000001_init.up.sql` defines `role` ENUM as `('participant', 'jury', 'admin')`. However, Product Specification and Capstone Register specify roles as `Candidate` and `Admin`.
- **Status:** `OPEN` (Identified gap in [[Technical-Debt-and-Gaps]])
- **Resolution Link:** Unresolved
