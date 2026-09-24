---
title: RoleCue Domain Brain
tags:
  - brain
  - documentation
  - architecture
  - domain-knowledge
aliases:
  - RoleCue Brain
  - SEP490 Domain Brain
---

# RoleCue Domain Knowledge Base

Welcome to the **RoleCue Domain Knowledge Base** (Brain). This repository serves as the single canonical source of durable business domain knowledge, concepts, invariants, and long-lived product decisions for the RoleCue platform.

---

## 1. Brain Philosophy

This repository is intentionally maintained as a **durable domain knowledge base**, not an operational project management tracker or a code mirror.

### What This Brain Answers
* **What is RoleCue?** The purpose, value proposition, and boundaries of the platform.
* **What problem does it solve?** Pain points in modern technical interview preparation and technical hiring practice.
* **What are its business domains?** The functional boundaries separating identity, job descriptions, job postings & applications, interview simulation, avatar & voice synthesis, evaluation, payment, and administration.
* **What are the core concepts?** Unambiguous definitions of Target JDs, Job Postings, Blueprints, Sessions, Voice Profiles, and Avatars.
* **How do those concepts relate?** Entity relationships, data flows, and conceptual cardinality.
* **What are the important product invariants and long-lived decisions?** Immutable rules that govern how the platform behaves.

### What This Brain Does NOT Answer
* Operational task progress ("What task are we doing today?", "What sprint are we in?") $\rightarrow$ Managed in **Jira**.
* Execution dependencies ("What KAN ticket depends on what?") $\rightarrow$ Managed in **Jira**.
* Git implementation state ("What PR is merged?", "What code file currently exists?") $\rightarrow$ Managed in the **Code Repository**.
* Working academic deliverables ("What report section is being edited?") $\rightarrow$ Managed in **Google Drive**.

---

## 2. Platform Summary

**RoleCue** is an AI-powered virtual technical interview simulation platform. It delivers realistic, personalized technical interview practice tailored to target Job Descriptions through:
* **AI-based JD Extraction & Refinement:** Ingestion of text or PDF job descriptions, deterministic validation of technical competencies, and natural-language candidate refinement.
* **Internal Interview Blueprint Generation:** Autonomous generation of comprehensive assessment plans hidden from the candidate.
* **Real-Time 3D Virtual Interviewer:** Interactive WebGL avatar with real-time speech-to-text (STT), text-to-speech (TTS), and synchronized blend-shape viseme lip-sync.
* **Adaptive Technical Probing:** Dynamic conversational dialogue that dives deeper based on candidate answers and blueprint criteria.
* **Post-Interview Evaluation:** Automated multi-dimensional scoring across 5 core competencies with actionable gap analysis.
* **Lightweight Job Posting & Application:** A streamlined recruiter board allowing candidate applications, bounded strictly at Application Approve/Reject.

---

## 3. Repository Map

The knowledge base is structured into four core directories:

```text
ai-interview-practice-brain/
├── README.md
├── 00_Project/                 # Product definition, actors, flows, and terminology
│   ├── Overview.md             # Core problem, value proposition, and boundaries
│   ├── Actors-and-Capabilities.md # The 6 actors and 58 use-case capability mapping
│   ├── Core-Flows.md           # End-to-end user journeys (Practice, Application, Avatar)
│   └── Glossary.md             # Locked domain terminology and distinction rules
├── 01_Domains/                 # Deep domain specifications & invariants
│   ├── Auth/README.md          # Identity, credentials, and access control
│   ├── Job-Description/README.md # Ingestion, extraction, review, and refinement
│   ├── Job-Posting-Application/README.md # Recruiter job postings & candidate applications
│   ├── Interview/README.md     # Real-time simulation, configuration, and blueprint engine
│   ├── Avatar-Voice/README.md  # 3D avatar rendering, personal photo avatars, and TTS voices
│   ├── Evaluation/README.md    # 5 core competencies, scoring rubrics, and roadmaps
│   ├── Payment/README.md       # Practice credits, recruiter memberships, and VAT invoicing
│   └── Administration/README.md # Platform governance, voice catalog, and telemetry
├── 02_System/                  # System-level models and architectural boundaries
│   ├── Context.md              # External actors and service boundaries
│   ├── Domain-Model.md         # Conceptual entity-relationship diagram
│   ├── Integrations.md         # LLM, STT, TTS, Payment Gateway, and Email integration
│   └── Data-Relationships.md   # Cardinalities, ownership, and cascading rules
└── 03_Decisions/               # Long-lived product and architectural decisions
    └── Product-Decisions.md    # Ratified foundational decisions
```

---

## 4. Reading Guide

* **New to the project?** Start with [[00_Project/Overview|Project Overview]], review [[00_Project/Actors-and-Capabilities|Actors & Capabilities]], and read [[00_Project/Core-Flows|Core Flows]].
* **Confused about terminology?** Consult the [[00_Project/Glossary|Domain Glossary]] for strict definitions (e.g., Target JD vs. Job Posting, Extracted JD vs. Blueprint).
* **Designing or understanding a feature?** Explore the relevant domain in [[01_Domains/Auth/README|01_Domains]].
* **Examining system boundaries & integrations?** See [[02_System/Context|Context Diagram]] and [[02_System/Integrations|External Integrations]].
* **Understanding foundational architectural constraints?** Read [[03_Decisions/Product-Decisions|Product Decisions]].
