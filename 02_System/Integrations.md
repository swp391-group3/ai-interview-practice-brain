---
title: External Integrations
tags:
  - system
  - integrations
  - llm
  - stt
  - tts
  - payment-gateway
  - email
aliases:
  - Integrations
  - External Services
---

# External Service Integrations

This document specifies the integration architecture, operational requirements, and fault-tolerance policies for external third-party service providers connected to RoleCue.

---

## 1. Architectural Integration Principles

1. **Vendor Agnosticism:**
   Core domain entities and business workflows must never depend directly on vendor-specific SDKs or proprietary JSON schemas. All external integrations are encapsulated behind internal interface adapters.
2. **Deterministic Pre/Post Validation:**
   Outputs from external AI providers (LLM extractions, STT transcripts) are treated as untrusted data. They must undergo deterministic schema validation and sanitization before entering domain persistence.
3. **Graceful Fallback:**
   When an external service experiences transient latency spikes or network timeouts, the platform must degrade gracefully without corrupting persisted session state or dropping conversation history.

---

## 2. Integration Catalog

```mermaid
flowchart LR
    subgraph Core["RoleCue Core Domain"]
        JD["JD Ingestion"]
        INT["Interview Engine"]
        EVAL["Evaluation Engine"]
        BILL["Membership & Payments"]
    end

    subgraph Adapters["Integration Adapters"]
        A_LLM["LLM Adapter"]
        A_STT["STT Adapter"]
        A_TTS["TTS Adapter"]
        A_PAY["Payment Adapter"]
        A_MAIL["Email Adapter"]
    end

    subgraph Providers["External Providers"]
        P_LLM["LLM Provider<br/>(Semantic Extraction, Dialogue, Evaluation)"]
        P_STT["STT Provider<br/>(Speech-to-Text)"]
        P_TTS["TTS Provider<br/>(Text-to-Speech & Visemes)"]
        P_PAY["Payment Gateway<br/>(Electronic Checkout & Webhooks)"]
        P_MAIL["Email Provider<br/>(Transactional Mail & Notices)"]
    end

    JD --> A_LLM
    INT --> A_LLM
    INT --> A_STT
    INT --> A_TTS
    EVAL --> A_LLM
    BILL --> A_PAY
    BILL --> A_MAIL

    A_LLM <--> P_LLM
    A_STT <--> P_STT
    A_TTS <--> P_TTS
    A_PAY <--> P_PAY
    A_MAIL --> P_MAIL
```

---

## 3. Provider Specifications

### 3.1. Large Language Model (LLM) Provider
* **Purpose:**
  * **Structured JD Extraction:** Parses unstructured job description text into validated JSON technical competencies (title, seniority, categorized skills, technologies).
  * **Interview Planning:** Autonomously builds the internal, hidden Interview Blueprint from approved requirements, refinement notes, and configuration parameters.
  * **Adaptive Conversational Probing:** Analyzes candidate speech turns in real time to generate contextual technical follow-up questions or transition between blueprint competency slots.
  * **Multi-Dimensional Evaluation:** Evaluates full session transcripts against blueprint rubrics across the 5 Core Competencies.
* **Fault Handling:**
  * If extraction fails or outputs an invalid schema, the system retries with adjusted parameters; surfaces an extraction failure if unresolvable.
  * If real-time probing times out during a live turn, the interview engine falls back to pre-budgeted default questions from the blueprint.

### 3.2. Speech-to-Text (STT) Provider
* **Purpose:**
  Transcribes incoming candidate audio stream chunks into clean text transcripts during live interview simulations.
* **Fault Handling:**
  In the event of partial packet loss or STT dropouts, the system prompts the candidate or allows speech retry to maintain conversational continuity.

### 3.3. Text-to-Speech (TTS) Provider
* **Purpose:**
  Synthesizes realistic spoken interviewer audio from generated question text and produces synchronized blend-shape viseme timing metadata.
* **Requirements:**
  * Must support returning speech audio paired with viseme timing metadata for facial blend-shape animation.
  * Must support multiple voice styles (cataloged and managed as Admin-governed Voice Profiles).
* **Fault Handling:**
  If the TTS stream fails, the session can display the question as text while attempting audio reconnection, avoiding an abrupt session abort.

### 3.4. Payment Gateway
* **Purpose:**
  Facilitates secure electronic payment processing for candidate membership subscriptions.
* **Provider Flexibility:**
  Supports localized payment rails and international card processors.
* **Security & Invariants:**
  * Webhook callbacks must be cryptographically signed by the gateway.
  * Webhook handlers must verify signatures and maintain strictly idempotent processing to prevent duplicate status changes or activations.
  * Subscription activations and transaction state updates must execute within database transactions.

### 3.5. Email Provider
* **Purpose:**
  Dispatches transactional system emails:
  * Account registration verification tokens.
  * Password recovery links.
  * Application submission confirmations and status change notices (Approved/Rejected).
  * Security alerts and account notifications.
* **Operational Invariants:**
  Asynchronous queue-based dispatch; failures in email delivery must never block core transactional API flows.
