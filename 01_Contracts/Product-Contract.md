---
project: SEP490
type: contract
status: draft
authority: team
last_verified: 2026-09-18
---

# Product Contract — RoleCue Platform

## 1. Status & Metadata
- **Status:** `DRAFT` (Core vision approved via Capstone Register; detailed feature specs under refinement)
- **Product Name:** RoleCue
- **Project Code:** `09_GFA26SE84`
- **Target Personas:** Candidate, Administrator

## 2. Scope & Core Value Proposition
RoleCue is an AI-powered technical mock interview simulation platform providing realistic, JD-tailored interview practice:
1. **JD Personalization:** Interviews are generated directly from candidate-provided Job Descriptions (text or PDF).
2. **Interactive AI Avatar:** Real-time conversational interview conducted by a 3D animated virtual avatar with speech and lip-sync.
3. **Adaptive Questioning:** Dynamic follow-up probing based on candidate answers and JD requirements.
4. **Structured Evaluation:** Granular post-interview assessment covering 5 competencies: Technical Accuracy, Depth of Understanding, Problem-Solving, Answer Relevance, Communication Clarity.

## 3. Core System Boundaries
- **Candidate User Journey (Report 2 v0.2 requirement order):**
  `Auth` -> `JD input/analyze` -> `Candidate review/edit` -> `save reviewed JD` -> `Interview Configuration` -> `Blueprint generation/preview` -> `Interview Session` -> `Evaluation Report` -> `History`.
- **Admin User Journey:**
  `Auth` -> `User/Account Management` -> `Session Monitoring` -> `Domain/Taxonomy Configuration` -> `Avatar/Voice Catalog` -> `Platform Analytics`.

## 4. Invariants
- Candidates can only access their own JDs, interview sessions, reports, and billing data.
- An interview session cannot start without an approved and persisted Job Description blueprint.
- Evaluation reports must strictly score against the technical expectations extracted from the associated JD.

## 5. Error & Fallback Behavior
- If 3D rendering fails on low-end client devices, system must offer an audio-only fallback mode.
- If external LLM or voice API times out during an interview, the session must pause gracefully without corrupting completed turn transcripts.

## 6. Academic traceability and design gaps

Report 2 v0.2 defines the FE-01–FE-12 WBS and confirms that reviewed JD precedes blueprint generation; configured difficulty is distinct from JD seniority. Report 3 v0.2 defines UC-C01–UC-C10, UC-A01–UC-A07, 19 top-level screens, and separate non-screen AI/voice/payment capabilities.

- **DESIGN/SRS GAP:** Registration is required by FE-01.1 and UC-C01, but Report 3's screen inventory lists Login without a dedicated Registration screen.
- **DESIGN/SRS GAP:** Candidate Dashboard is listed and used as navigation origin but lacks a comparably detailed screen subsection.
- **CONTRADICTION:** Report 3 places blueprint preview in Review Extracted Requirements; Report 2 and KAN-46 direct review → configuration → blueprint generation/preview. Current product reasoning uses the latter sequence unless a team decision changes it.
- **Granularity rule:** avatar/interviewer/voice selection may be design substeps within Interview Configuration, not additional SRS top-level screens without explicit acceptance.

## 7. Open Questions
- Exact billing tiers and free-tier credit allowances (see [[Open-Questions]] OQ-08).
- Role naming consensus: `participant` vs. `Candidate` (see [[Open-Questions]] OQ-09).

## 8. Traceability
- **Relevant Jira:** [[KAN-46]], [[KAN-18]], [[KAN-19]], [[KAN-20]]
- **Relevant Decisions:** [[ADR-001-backend-directory-and-package-structure]], [[Decision-Registry]]
- **Reference Material:** [[08_Reports/Lecturer/9_GFA26SE84_AI_Virtual_Technical_Interview_Capstone_Register.pdf]]
- **Current academic deliverables:** `08_Reports/Report-1-3/Report2_Project_Management_Plan_v0.2.docx`, `08_Reports/Report-1-3/Report3_Software_Requirement_Specification_v0.2.docx`
