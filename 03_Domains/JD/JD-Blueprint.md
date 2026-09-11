---
project: SEP490
type: domain
status: draft
authority: team
last_verified: 2026-09-11
---

# JD Interview Blueprint Specification

> **Tracking:** [[KAN-46]]  
> **Committed Deadline:** 2026-09-11 14:00  
> **Status:** `DRAFT / IN PROGRESS`

---

## 1. Problem Statement & Purpose
The Interview Blueprint is the core integration contract between the **JD Analysis Domain** and the **Live Interview Subsystem**. It determines:
- How many questions the AI interviewer will ask.
- What specific technical topics, frameworks, and architecture areas will be evaluated.
- The targeted difficulty level (Junior, Mid, Senior, Lead).
- The allocated time per interview section.
- The evaluation criteria against which the post-interview scoring engine will grade.

---

## 2. Proposed Blueprint Schema (Draft)

> [!NOTE]
> This schema is under active definition in [[KAN-46]]. Final fields are subject to team sign-off.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InterviewBlueprint",
  "type": "object",
  "required": ["blueprintId", "jdId", "targetRole", "seniority", "totalDurationMinutes", "stages"],
  "properties": {
    "blueprintId": { "type": "string", "format": "uuid" },
    "jdId": { "type": "string", "format": "uuid" },
    "targetRole": { "type": "string" },
    "seniority": { "type": "string", "enum": ["intern", "junior", "middle", "senior", "lead"] },
    "totalDurationMinutes": { "type": "integer", "minimum": 15, "maximum": 60 },
    "stages": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["stageIndex", "stageType", "title", "allocatedMinutes", "targetSkills", "questionBudget"],
        "properties": {
          "stageIndex": { "type": "integer" },
          "stageType": { "type": "string", "enum": ["introduction", "technical_deep_dive", "system_design", "behavioral", "wrap_up"] },
          "title": { "type": "string" },
          "allocatedMinutes": { "type": "integer" },
          "targetSkills": { "type": "array", "items": { "type": "string" } },
          "questionBudget": { "type": "integer" }
        }
      }
    },
    "evaluationRubric": {
      "type": "object",
      "properties": {
        "competencies": { "type": "array", "items": { "type": "string" } },
        "passThreshold": { "type": "number" }
      }
    }
  }
}
```

---

## 3. Invariants
- An interview blueprint is generated after candidate review of extracted skills.
- The blueprint is frozen upon candidate confirmation; live interview sessions reference this immutable snapshot.
- Blueprint generation must strictly map to skills present in the persisted JD.
