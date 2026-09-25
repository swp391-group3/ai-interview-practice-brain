---
title: Project Overview
tags:
  - project
  - overview
  - scope
  - product-boundary
aliases:
  - Overview
  - Product Overview
---

# Project Overview — RoleCue Platform

**RoleCue** is an AI-powered virtual technical interview simulation platform designed to bridge the gap between static self-study and high-stakes real-world technical interviews.

---

## 1. The Problem

Technical interview preparation is critical for career progression in software engineering, yet traditional preparation mechanisms suffer from severe structural shortcomings:

1. **Lack of Job Description (JD) Personalization:**
   Traditional platforms (e.g., LeetCode, generic question banks) present static, disconnected algorithmic puzzles. They fail to align with the specific tech stack, architecture patterns, domain constraints, and seniority expectations of a candidate's target job opening.
2. **Limited Availability of Expert Interviewers:**
   Scheduling realistic mock interviews with senior engineers or mentors is prohibitively expensive, difficult to coordinate, and rarely repeatable at scale.
3. **Absence of Real-Time Conversational Pressure:**
   Static multiple-choice quizzes and automated code grading do not prepare candidates for live technical dialogue. Candidates struggle to articulate trade-offs, explain system design rationale, and handle spontaneous interviewer Questions under time constraints.
4. **Superficial & Non-Actionable Feedback:**
   Existing tools provide binary pass/fail outcomes or generic scores. Candidates are left without insight into their root-cause conceptual gaps, technical depth, problem-solving methodology, or concrete study roadmaps.

---

## 2. Core Value Proposition

RoleCue solves these challenges by combining AI semantic parsing, generative conversational intelligence, real-time speech processing, and interactive 3D WebGL graphics into an end-to-end interview simulation experience:

* **Targeted Practice:** Practice against the exact Job Description a candidate is targeting.
* **Realistic Pressure:** Converse face-to-face with an animated 3D virtual interviewer using natural spoken voice.
* **Intelligent Questioning:** Experience an adaptive sequence of Questions determined from each answer and the internal interview context.
* **Objective Diagnostic Feedback:** Receive immediate, granular scoring across 5 core technical competencies accompanied by turn-by-turn critiques and personalized learning roadmaps.

---

## 3. Product Users & Personas

RoleCue is designed for four primary user groups:

| Actor | Profile | Primary Motivation |
| :--- | :--- | :--- |
| **Candidate** | Software engineers, students, career switchers | Prepare for specific technical job interviews, assess technical readiness, configure and conduct mock interviews, create a personal 3D avatar through Avaturn, manage membership, and discover matching job postings. |
| **Recruiter** | Tech talent acquisition, hiring managers, company reps | Publish company Job Postings to attract qualified candidates and screen incoming applications. |
| **Guest** | Unauthenticated visitors, prospective users | View the public landing page and register for an account. |
| **Administrator** | Platform operators, technical governance | Maintain account security, approve/reject job postings, oversee interview sessions, calibrate AI behavior and evaluation criteria, curate TTS voice profiles, track membership revenue, and update membership prices. |

> [!NOTE]
> System semantics also recognize **Registered User** (the shared authentication and profile base for Candidates and Recruiters) and **System Handler** (the internal automated handler responsible for terminating a candidate's abandoned session). Neither is an external actor.

---

## 4. Major Product Capabilities

RoleCue organizes its capabilities into six core functional pillars:

```mermaid
flowchart TD
    subgraph Ingestion["1. JD Ingestion & Refinement"]
        JD1["Raw Target JD (Text/PDF)"] --> JD2["AI Competency Extraction"]
        JD2 --> JD3["Candidate Review & Refinement Notes"]
        JD3 --> JD4["Approved Extracted JD"]
    end

    subgraph Planning["2. Assessment Planning"]
        JD4 --> BP1["Internal Interview Blueprint Generation<br/>(Hidden from Candidate)"]
        CFG["Composite Interview Configuration"] --> BP1
    end

    subgraph Simulation["3. Virtual Simulation"]
        BP1 --> SIM1["3D Virtual Interviewer (WebGL)"]
        SIM1 <--> SIM2["Real-Time Speech Interaction (STT / TTS)"]
        SIM2 <--> SIM3["LLM-Determined Question Loop"]
    end

    subgraph Evaluation["4. Multi-Dimensional Evaluation"]
        SIM3 --> EV1["Automated Turn Grading"]
        EV1 --> EV2["5-Competency Radar & Score"]
        EV2 --> EV3["Actionable Learning Roadmap"]
    end

    subgraph Board["5. Lightweight Job Board"]
        REC["Approved Recruiter Job Postings"] <--> APP["Candidate Applications<br/>(CV + Interview Result)"]
        APP --> DEC["Approve / Reject Decision"]
    end

    subgraph Identity["6. 3D Identity & Membership"]
        AVATURN["Embedded Avaturn Experience"] --> AVA["RoleCue VRM Personal Avatar"]
        PAY["Candidate Membership Subscription"] --> TRANS["Payment Transactions & Governance"]
    end
```

1. **Job Description Extraction & Refinement:**
   Ingests raw text or multi-page PDF documents. Extracts normalized technical competencies (languages, frameworks, databases, tools, domain knowledge, seniority). Empowers the candidate to review extracted tags and provide natural-language refinement notes (e.g., *"Exclude C# from the interview"*).
2. **Internal Interview Blueprint Generation:**
   Translates the approved JD, candidate refinement notes, and interview configuration into a comprehensive, structured assessment plan. Specifies topic matrices, question slots, depth thresholds, and rubrics. **The blueprint remains strictly internal and hidden from the candidate.**
3. **Real-Time 3D Virtual Interview Simulation:**
   Renders a 3D animated avatar in the browser via WebGL. The system obtains the next Question, TTS delivers it with synchronized blend-shape viseme lip-sync, STT transcribes the Candidate's answer, and the LLM uses that Answer with the internal Interview Context to determine the next Question. For MVP, the LLM makes this decision; there is no separate Decision Layer.
4. **Automated Multi-Dimensional Evaluation:**
   Grades completed sessions across 5 core competencies: *Technical Accuracy*, *Depth of Understanding*, *Problem-Solving*, *Answer Relevance*, and *Communication Clarity*. Generates comprehensive performance reports with radar charts and personalized improvement roadmaps.
5. **Lightweight Job Posting & Application:**
   Enables Recruiters to create, update, and archive Job Postings (company JDs), select a company 3D interviewer model and Voice Profile, and submit postings for Admin approval. Candidates can browse approved postings, upload a CV/resume, complete the required technical interview using the locked company configuration, and submit an Application containing the resulting Interview Result. Recruiters search applications and render a final **Approve** or **Reject** decision.
6. **Personal 3D Avatar Generation & Customization:**
   RoleCue embeds the free Avaturn iframe experience, where Avaturn handles three-photo capture, validation, preview generation, and customization before returning the final GLB. RoleCue converts that GLB to VRM, persists the Candidate-owned personal avatar, and uses VRM as the production artifact. For Target JD interviews, Candidates can choose an available system 3D interviewer or eligible personal 3D model, an available Voice Profile, and a 3D environment. Job Posting interviews use the company-defined model and Voice Profile without Candidate override.

---

## 5. Product Scope Boundaries

To maintain focus on interview simulation and delivery excellence, RoleCue establishes strict, long-lived boundaries:

### What RoleCue IS NOT:
* **NOT a Full Applicant Tracking System (ATS):**
  RoleCue provides a lightweight job board and application submission workflow, but recruitment scope strictly terminates at **Application Approve / Reject**. RoleCue does **NOT** support multi-stage hiring funnels, interview panel scheduling, offer letter generation, salary negotiations, background checks, or employee onboarding.
* **NOT an Autonomous Hiring Decision Engine:**
  RoleCue does not rank applicants for employers, eliminate candidates automatically, or make official employment decisions. It is an educational practice simulator and pre-application preparation platform.
* **NOT a Multi-Tenant SaaS:**
  RoleCue does not employ a complex multi-tenant architecture. There are no tenant schemas, no Row-Level Security (RLS) tenant isolation policies, and no organization workspace hierarchies. Recruiter accounts associate with company metadata via simple relational foreign keys.
* **NOT a 3D Asset Marketplace:**
  There is no community asset store, creator marketplace, or user-published 3D model sharing. Avatars and environments are curated platform presets or candidate-generated personal avatars.
* **NOT a Soft-Skills or Behavioral Grader:**
  JD extraction, blueprint generation, and interview scoring concentrate strictly on **technical competencies**. Personality analysis, micro-expression tracking, and non-technical behavioral scoring are intentionally excluded.

---

## 6. Document Cross-References
* Actors & Use Cases: [[00_Project/Actors-and-Capabilities|Actors and Capabilities]]
* Core Workflows: [[00_Project/Core-Flows|Core Flows]]
* Terminology Standards: [[00_Project/Glossary|Glossary]]
* System Architecture: [[02_System/Context|System Context]] & [[02_System/Domain-Model|Domain Model]]
* Long-Lived Decisions: [[03_Decisions/Product-Decisions|Product Decisions]]
