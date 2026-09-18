# KAN-18 — Raw JD to Validated StructuredJD

> **Artifact:** `kan18-jd-extraction-flow.html`  
> **Source Spec:** `kan18-jd-extraction-flow.json`  
> **Archify Profile:** `showcase` (9/9 checks passed, 0 errors, 0 warnings, verified containment at 1440×900, 1600×1000, 1920×1080, 2048×1320)  
> **Diagram Type:** `architecture`  

---

## Overview

Visualizes the complete lifecycle of Job Description (JD) processing under **KAN-18: JD Domain Model and Structured LLM Extraction**.

```
Raw JD Text (untrusted)
  ↓
JD Service Orchestrator (Service.Extract)
  ↓
Input Normalization & Pre-Validation (NormalizeInput: 100–20,000 runes)
  ↓
Extractor Port (service.Extractor)
  ↓
OpenAI Adapter (provider.OpenAI: 1 MiB cap, strict JSON)
  ↓
External LLM (Google Gemini Developer API: gemini-3.1-flash-lite)
  ↓
ExtractionCandidate (untrusted model proposal)
  ↓
Candidate Validation & Normalization (ValidateCandidate: schema, enums, deduplication)
  ↓
StructuredJD (trusted domain-validated entity)
```

---

## Trust Boundaries & Validation

- **UNTRUSTED:**
  - `Raw JD`: Plain text from external client / future KAN-19 HTTP handler.
  - `Google Gemini Developer API`: External generative AI model.
  - `ExtractionCandidate`: Raw model proposal, untrusted even when JSON envelope decoding succeeds.
- **TRUSTED:**
  - `NormalizeInput`: Deterministic UTF-8 verification, CRLF normalization, whitespace collapsing, and 100–20,000 Unicode rune enforcement. Invalid input stops immediately and **never invokes the LLM**.
  - `ValidateCandidate`: Deterministic schema validation, category/requirement/seniority enums, whitespace trimming, case-insensitive deduplication, conflict rejection, and nonblank competency guarantee.
  - `StructuredJD`: Immutable, domain-validated entity representing the final output contract of KAN-18.

---

## Retry Budget & Error Contract

- **Retry Budget:** `LLM_MAX_RETRIES = 0 or 1` (maximum 2 total attempts with 100 ms backoff).
- **Transport Abstraction:** Provider `HTTPError` implements `RetryableFailure` (retrying HTTP 429, 500, 502, 503, 504). The domain service stays completely HTTP-agnostic.
- **Shared Budget:** Covers both transient network errors and `INVALID_EXTRACTION_OUTPUT` regeneration.
- **No Retry:** Invalid raw input, `context.Canceled`, `context.DeadlineExceeded`, and permanent client errors.
- **Error Codes (`api/pkg/apperror/apperr.go`):**
  - `INVALID_JD_INPUT`
  - `JD_TOO_SHORT`
  - `EXTRACTION_FAILED`
  - `INVALID_EXTRACTION_OUTPUT`

---

## Scope Boundaries

- **In Scope (KAN-18):** Raw text normalization, LLM provider integration, candidate extraction, deterministic domain validation, StructuredJD model creation.
- **Out of Scope (Downstream):**
  - REST API / HTTP transport mapping (KAN-19)
  - PostgreSQL database persistence (KAN-19)
  - PDF document parsing (KAN-44)
  - Blueprint generation
  - Interview questions & adaptive follow-up
  - Session runtime

---

## Files

- **Interactive Viewer:** [`kan18-jd-extraction-flow.html`](kan18-jd-extraction-flow.html)
- **Specification:** [`kan18-jd-extraction-flow.json`](kan18-jd-extraction-flow.json)
- **Contact Sheet Evidence:** [`kan18-jd-extraction-flow.visual-check.html`](kan18-jd-extraction-flow.visual-check.html)
