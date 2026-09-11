---
project: SEP490
type: execution
status: open
authority: jira
last_verified: 2026-09-11
---

# KAN-20: Build JD Upload, Editable Skill Review and Blueprint Preview UI

## 1. Metadata
- **Key:** `KAN-20`
- **Component:** Frontend / Candidate Experience
- **Committed Deadline:** **2026-09-14 23:59**
- **Status:** `QUEUED` (Depends on [[KAN-19]])

## 2. Goal & Intent
Build the Next.js multi-step wizard allowing candidates to upload/paste a Job Description, review and edit the extracted skills, and preview the generated interview blueprint before launching an interview.

## 3. Acceptance Criteria
- [ ] File dropzone for PDF upload + raw text input area.
- [ ] Loading indicator during backend extraction.
- [ ] Interactive skill editor: candidates can add tags, delete tags, and modify seniority.
- [ ] Blueprint summary preview showing stages, question counts, and duration.
- [ ] Connected to backend endpoints via `frontend/src/lib/api/transport.ts` and React Query.
- [ ] Adheres to RoleCue design tokens and components.

## 4. Open Questions / Missing Decisions
- Exact URL route path for the wizard steps? `[OPEN / NEEDS TEAM DECISION]`
