---
project: SEP490
type: domain
status: draft
authority: team
last_verified: 2026-09-11
---

# Candidate JD Frontend Workflow

> **Tracking:** [[KAN-20]]  
> **Committed Deadline:** 2026-09-14 23:59  
> **Status:** `QUEUED`

---

## 1. User Interface Flow

```
Step 1: Input / Upload
  ├── Option A: Paste raw job description text into textarea
  └── Option B: Drag & drop PDF file
         │
         ▼
Step 2: Processing Spinner / Loading State
  └── "RoleCue AI is analyzing your job description..."
         │
         ▼
Step 3: Interactive Skill & Requirement Review
  ├── Edit job title & seniority badge
  ├── Review categorized skill tags (Languages, Databases, Cloud)
  ├── Add missing skills / delete irrelevant extracted skills
  └── Confirm & Proceed
         │
         ▼
Step 4: Blueprint Preview & Interview Launch
  ├── Review interview stages, question count, estimated duration
  └── Click "Start Mock Interview" -> routes to 3D Virtual Room
```

---

## 2. Component Structure (`frontend/src/features/job-description`)
```
frontend/src/features/job-description/
├── components/
│   ├── jd-upload-card.tsx         # File dropzone & textarea inputs
│   ├── skill-badge-editor.tsx     # Add/remove skill tags with importance toggle
│   ├── blueprint-preview.tsx      # Stage timeline, duration, question budget
│   └── jd-wizard-container.tsx    # Multi-step state orchestrator
├── api/
│   ├── requests.ts                # createApiTransport endpoints + Zod decoders
│   ├── keys.ts                    # React Query query keys
│   └── mutations.ts               # useMutation hooks for upload & update
└── types.ts                       # Domain types matching backend schemas
```

---

## 3. Invariants
- Candidate must see visual feedback if uploaded PDF exceeds 10MB or is invalid.
- Extracted skills must be editable before the candidate initiates blueprint generation.
