---
project: SEP490
type: execution
status: open
authority: jira
last_verified: 2026-09-11
---

# KAN-44: [Backend][JD] Implement JD PDF Extraction Pipeline

## 1. Metadata
- **Key:** `KAN-44`
- **Component:** Backend / Ingestion
- **Committed Deadline:** **2026-09-12 18:00**
- **Status:** `QUEUED`

## 2. Goal & Intent
Implement a decoupled, standalone Go component that ingests PDF file bytes and extracts sanitized, readable UTF-8 plain text.

## 3. Acceptance Criteria
- [ ] Reads PDF from byte slice or multipart file reader.
- [ ] Extracts text across multi-page documents in sequential order.
- [ ] Strips null bytes and invalid UTF-8 characters.
- [ ] Gracefully returns an error (`apperror.CodeValidation`) for encrypted, password-protected, or unreadable PDFs.
- [ ] **Decoupling invariant:** Must NOT execute LLM logic directly; pure text extraction only.

## 4. Open Questions / Missing Decisions
- PDF parsing library in Go: `pdfcpu` vs. `ledongthuc/pdf` vs. system `pdftotext`? `[OPEN]`
