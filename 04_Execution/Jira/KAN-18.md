---
project: SEP490
type: execution
status: open
authority: jira
last_verified: 2026-09-11
---

# KAN-18: Implement JD Domain Model and Structured LLM Extraction

## 1. Metadata
- **Key:** `KAN-18`
- **Component:** Backend / AI Integration
- **Committed Deadline:** **2026-09-11 23:59**
- **Status:** `PENDING KAN-46`

## 2. Goal & Intent
Implement Go domain structs and LLM prompt orchestration to extract technical skills, tools, frameworks, seniority level, and role summary from raw job description text.

## 3. Acceptance Criteria
- [ ] Domain entity `ExtractedJD` defined in Go.
- [ ] LLM client sends clean text and receives structured, validated JSON output.
- [ ] Basic validation to catch schema mismatch or missing mandatory fields.
- [ ] Unit tests verifying extraction parsing with sample text.

## 4. Open Questions / Missing Decisions
- LLM provider and model selection: OpenAI vs. Gemini vs. Claude? `[OPEN / NEEDS DECISION]`
- Prompt versioning and storage strategy? `[OPEN]`
