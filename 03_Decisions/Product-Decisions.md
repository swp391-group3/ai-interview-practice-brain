---
title: Foundational Product Decisions
tags:
  - decisions
  - product-decisions
  - architecture
  - invariants
aliases:
  - Product Decisions
  - Long-Lived Decisions
---

# Foundational Product Decisions

This document records the ratified, long-lived product decisions that govern the architecture, domain boundaries, and user experiences of RoleCue. These decisions serve as permanent interpretive guidelines for engineering and product design.

---

## 1. Blueprint is Internal & Hidden from Candidate
* **Decision:** The Interview Blueprint is a first-class **internal** domain concept that is strictly hidden from the Candidate.
* **Rationale:** Exposing the blueprint (with its question slots, expected technical benchmarks, and grading criteria) would turn the mock interview into an artificial "memorize-the-rubric" exercise rather than an authentic, adaptive simulation. The Candidate experiences the interview naturally through spoken dialogue.
* **Rule:** Candidates never view, edit, or directly confirm an Interview Blueprint.

---

## 2. Candidate Refinement Happens Before Blueprint Generation
* **Decision:** Candidates review and refine the AI-extracted technical competencies (and may provide natural-language refinement notes, such as *"Exclude C# from the interview"*) **before** the system compiles the Interview Blueprint.
* **Rationale:** The blueprint generator requires confirmed, human-verified requirements and explicit candidate instructions to build a high-quality assessment plan.
* **Rule:**
  $$\text{Approved Extracted JD} + \text{Refinement Notes} + \text{Configuration} \longrightarrow \text{Interview Blueprint}$$

---

## 3. Job Posting is the Recruiter's Company JD
* **Decision:** The `Job Posting` entity represents the employer's Job Description. A separate "Corporate JD" entity is **not** created.
* **Rationale:** Introducing both "Corporate JD" and "Job Posting" creates redundant entities and semantic ambiguity. A Recruiter's Job Posting serves as both the public job board opening and the underlying company JD.
* **Rule:** Maintain single canonical naming: `Job Posting`.

---

## 4. Recruiter Workflow Stops at Application Approve / Reject
* **Decision:** The recruitment workflow for Recruiters strictly terminates at **Application Approve** or **Reject**.
* **Rationale:** RoleCue is an interview practice simulator and lightweight career matching board, not a monolithic talent acquisition suite. Modeling multi-stage hiring pipelines, panel scheduling, or onboarding would dilute team focus and explode project complexity.
* **Rule:** An application has only two terminal states: `APPROVED` or `REJECTED`.

---

## 5. RoleCue is NOT a Full ATS
* **Decision:** RoleCue explicitly disclaims full Applicant Tracking System (ATS) functionality.
* **Rationale:** Full ATS platforms require complex compliance workflows, candidate ranking algorithms, integration with HRIS systems, offer letter workflows, and background check integrations. RoleCue deliberately excludes these.
* **Rule:** RoleCue does not rank applicants for employers, automate hiring decisions, or manage hiring funnels.

---

## 6. Configure Interview Session is a Composite Capability
* **Decision:** `Configure Interview Session` is modeled as a single composite capability encompassing interviewer persona, voice profile, 3D room environment, difficulty, and question budget.
* **Rationale:** Breaking visual, vocal, environmental, and difficulty settings into separate top-level use cases adds unnecessary administrative overhead. The user configures their session in a cohesive wizard.
* **Rule:** Interview configuration is a unified setup step, not fragmented use cases.

---

## 7. Personal 3D Avatar from Photo is Accepted Scope
* **Decision:** Generating a personal 3D avatar from a single candidate portrait photograph is an accepted product capability.
* **Rationale:** Technical feasibility was conclusively demonstrated during the **Avaturn** integration spike, which proved that single-image reconstruction can yield rigged 3D humanoid meshes compatible with WebGL.
* **Rule:** Treat photo-to-avatar generation as accepted product scope; do not describe it as speculative or failed.

---

## 8. Admin Manages Voice Profiles, but NOT 3D Avatars or Environments
* **Decision:** The Administrator manages the catalog of Voice Profiles sourced from TTS providers, but does **NOT** manage the 3D avatar catalog or 3D background scenes.
* **Rationale:** 3D avatar meshes and WebGL environment scenes require 3D modeling, vertex optimization, and collision rigging, making ad-hoc administrative uploads impractical. Conversely, TTS voice profiles simply reference provider API identifiers and string metadata, which are safe and practical for admin curation.
* **Rule:** 3D avatars and environments are built-in presets; Voice Profiles are admin-governed.

---

## 9. No Multi-Tenancy Architecture
* **Decision:** RoleCue operates on a single relational schema without multi-tenant architecture.
* **Rationale:** The platform does not require complex multi-tenant isolation (no tenant subdomains, tenant connection pools, tenant middleware, schema-per-tenant, or PostgreSQL Row-Level Security). Recruiter accounts link to company profile metadata via standard foreign keys.
* **Rule:** Avoid multi-tenant complexity; use straightforward relational associations.

---

## 10. No 3D Marketplace or Community Publishing
* **Decision:** 3D avatar marketplace, trading, and community model publishing are strictly excluded from the product.
* **Rationale:** A 3D asset marketplace introduces asset moderation, copyright liability, 3D mesh security scanning, and creator payout systems that fall outside RoleCue's core mission.
* **Rule:** Avatars are restricted to curated platform presets and candidate-generated personal avatars.
