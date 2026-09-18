---
project: SEP490
type: execution
status: done
authority: jira
last_verified: 2026-09-18
---

# KAN-18: JD Domain Model and Structured LLM Extraction

**Jira:** `DONE`. **MERGED IMPLEMENTATION:** feature-oriented JD extraction, Eino/Gemini configured model, strict JSON decoding, normalization, deterministic validation, and tests. The canonical schema is `title`, optional `seniorityLevel`, `skills`, `technologies`, and `domainKnowledge`; it deliberately excludes soft skills. See [[JD-Extraction]].
