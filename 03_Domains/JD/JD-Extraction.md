---
project: SEP490
type: domain
status: draft
authority: team
last_verified: 2026-09-11
---

# JD Structured LLM Extraction

> **Tracking:** [[KAN-18]]  
> **Committed Deadline:** 2026-09-11 23:59  
> **Status:** `PENDING KAN-46`

---

## 1. Objective
Transform raw UTF-8 job description text into a normalized, structured JSON schema containing technical skills, experience requirements, tools, and domain classifications.

---

## 2. Architecture & Pipeline
```
[Raw Clean JD Text] 
         │
         ▼
[System Prompt + Pydantic/Zod/Go JSON Schema]
         │
         ▼
[LLM Structured Output (JSON Mode)]
         │
         ▼
[Go Domain Validator: validate skills, normalize categories]
         │
         ▼
[Domain Entity: StructuredJD]
```

---

## 3. Extracted Entity Model (Draft)

```go
type ExtractedSkill struct {
    Name        string `json:"name"`
    Category    string `json:"category"` // "language", "framework", "database", "cloud_infra", "tool", "concept"
    Importance  string `json:"importance"` // "required", "preferred"
    Proficiency string `json:"proficiency"` // "basic", "intermediate", "advanced"
}

type ExtractedJD struct {
    JobTitle          string           `json:"jobTitle"`
    Seniority         string           `json:"seniority"`
    YearsOfExperience *int             `json:"yearsOfExperience"`
    Domain            string           `json:"domain"`
    Skills            []ExtractedSkill `json:"skills"`
    Responsibilities  []string         `json:"responsibilities"`
    RawSummary        string           `json:"rawSummary"`
}
```

---

## 4. Invariants & Error Handling
- **Hallucination Suppression:** Prompts must instruct the LLM to extract only explicitly stated or strongly implied technical skills, not invent entire stacks.
- **Failover:** If JSON decoding fails or required fields are missing, return `apperror.CodeValidation` with a descriptive message.
- **Open Decisions:** Provider selection (OpenAI vs. Gemini vs. Claude) remains `OPEN` (see [[Open-Questions]] OQ-05).
