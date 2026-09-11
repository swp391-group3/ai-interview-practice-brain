---
project: SEP490
type: domain
status: open
authority: team
last_verified: 2026-09-11
---

# JD PDF Ingestion Pipeline

> **Tracking:** [[KAN-44]]  
> **Committed Deadline:** 2026-09-12 18:00  
> **Status:** `QUEUED`

---

## 1. Architectural Principle: Pipeline Separation
The PDF extraction pipeline operates under a strict isolation contract:

```
┌─────────────────┐       ┌────────────────────────┐       ┌──────────────────────┐
│  Raw PDF Bytes  │  ──>  │  KAN-44: PDF Extractor  │  ──>  │ Clean UTF-8 Plain    │
│  (Uploaded File)│       │  (Library / Tooling)   │       │ Text (Raw String)    │
└─────────────────┘       └────────────────────────┘       └──────────────────────┘
                                                                       │
                                                                       ▼
                                                           ┌──────────────────────┐
                                                           │ KAN-18: LLM Parsing  │
                                                           │ Pipeline             │
                                                           └──────────────────────┘
```

> [!IMPORTANT]
> Do NOT couple PDF extraction directly to LLM prompt execution. The PDF component must only be responsible for reading byte buffers, extracting textual content, and sanitizing character encoding.

---

## 2. Invariants & Constraints
- **Maximum File Size:** 10 MB limit for uploaded PDF documents.
- **Format:** Strict MIME type check (`application/pdf`).
- **Clean Output:** Strip binary artifacts, normalize whitespace and line breaks.
- **Multi-page Support:** Concatenate text in natural page reading order.

---

## 3. Library Selection (Under Review - OQ-03)
- Pure Go candidates: `github.com/ledongthuc/pdf`, `rsc/pdf`, `pdfcpu`.
- System wrapper candidate: `pdftotext` (poppler-utils).
