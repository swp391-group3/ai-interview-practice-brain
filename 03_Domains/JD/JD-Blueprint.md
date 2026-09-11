---
project: SEP490
type: domain
status: draft
authority: team
last_verified: 2026-09-11
---

# JD Interview Blueprint Specification

> **Tracking:** [[KAN-46]]  
> **Authority:** LOCAL WORKING CONTRACT / PROPOSED TEAM CONTRACT (pending backend team review & ratification)  
> **Status:** `PROPOSED / IN PROGRESS`  

---

## 1. Canonical Terminology

To eliminate architectural ambiguity across team and domain boundaries, the following terms and responsibilities are canonical:

* **Job Description (JD):** What the target job requires. Extracted from raw text or uploaded PDF, reviewed/edited by the candidate, and persisted in `job_descriptions`.
* **Reviewed JD:** The candidate-approved requirements (skills, seniority, domain context) after human review/edit (`is_reviewed = true`). Serves as the authoritative basis for blueprinting.
* **Interview Config:** How the candidate wishes to configure their practice session (difficulty, duration, question count, optional focus areas, avatar selection).
* **Interview Blueprint:** The materialized assessment plan produced from Reviewed JD + Interview Config + Interview Policy. It defines **WHAT to assess** (competencies, stages, timing allocations, question budget, evaluation rubrics). It is **NOT** a fixed list of pre-generated interview questions.
* **Interview Session:** One runtime execution attempt of an Interview Blueprint (`interview_sessions`). A single Blueprint can be executed across multiple independent sessions (1:N).
* **Runtime Question:** A concrete adaptive question formulated dynamically during session turn-taking by the AI orchestrator (**HOW to ask**), tailored to candidate responses and blueprint objectives.

---

## 2. Conceptual Input Contract

Blueprint generation accepts a conceptual `BlueprintGenerationInput` object combining three distinct concerns:

```text
BlueprintGenerationInput {
    reviewedJd: {
        id: UUID,
        title: String,
        seniority: String,
        domainId: UUID (optional),
        requiredSkills: List<Skill>,
        preferredSkills: List<Skill>,
        summary: String
    },
    interviewConfiguration: {
        difficulty: String,             // e.g. "junior", "middle", "senior", "lead"
        durationMinutes: Integer,       // e.g. 15, 30, 45, 60
        questionCount: Integer,         // e.g. 5, 8, 10, 15
        focusAreas: List<String>        // optional user-selected technical topics
    },
    interviewPolicy: {
        maxStageMinutes: Map<StageType, Integer>,
        mandatoryStages: List<StageType>,
        rubricWeightBounds: Map<String, Range>,
        passThresholdDefault: Float
    }
}
```

> [!NOTE]
> Go struct definitions remain unfinalized until backend team ratification of KAN-46.

---

## 3. Conceptual Output Contract (Draft Blueprint Schema)

A generated and validated `InterviewBlueprint` defines the structured assessment plan:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InterviewBlueprint",
  "type": "object",
  "required": [
    "contractVersion",
    "blueprintId",
    "accountId",
    "jdId",
    "title",
    "configuration",
    "assessmentPlan",
    "evaluationPlan",
    "generationMetadata"
  ],
  "properties": {
    "contractVersion": { "type": "string", "enum": ["1.0.0-draft"] },
    "blueprintId": { "type": "string", "format": "uuid" },
    "accountId": { "type": "string", "format": "uuid" },
    "jdId": { "type": "string", "format": "uuid" },
    "title": { "type": "string" },
    "configuration": {
      "type": "object",
      "required": ["difficulty", "durationMinutes", "totalQuestionBudget"],
      "properties": {
        "difficulty": { "type": "string", "enum": ["junior", "middle", "senior", "lead"] },
        "durationMinutes": { "type": "integer", "minimum": 15, "maximum": 60 },
        "totalQuestionBudget": { "type": "integer", "minimum": 3, "maximum": 20 },
        "focusAreas": { "type": "array", "items": { "type": "string" } }
      }
    },
    "assessmentPlan": {
      "type": "object",
      "required": ["coverage", "stages"],
      "properties": {
        "coverage": { "type": "array", "items": { "type": "string" } },
        "stages": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["stageIndex", "stageType", "title", "allocatedMinutes", "questionBudget", "targetSkills", "expectedDepth"],
            "properties": {
              "stageIndex": { "type": "integer" },
              "stageType": { "type": "string", "enum": ["introduction", "technical_deep_dive", "system_design", "behavioral", "wrap_up"] },
              "title": { "type": "string" },
              "allocatedMinutes": { "type": "integer" },
              "questionBudget": { "type": "integer" },
              "targetSkills": { "type": "array", "items": { "type": "string" } },
              "expectedDepth": { "type": "string", "enum": ["conceptual", "practical", "architectural", "tradeoff"] }
            }
          }
        }
      }
    },
    "evaluationPlan": {
      "type": "object",
      "required": ["competencies", "passThreshold"],
      "properties": {
        "competencies": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "weight"],
            "properties": {
              "name": { "type": "string" },
              "weight": { "type": "number", "minimum": 0, "maximum": 1 }
            }
          }
        },
        "passThreshold": { "type": "number", "minimum": 0, "maximum": 10 }
      }
    },
    "generationMetadata": {
      "type": "object",
      "properties": {
        "version": { "type": "integer", "default": 1 },
        "createdAt": { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

---

## 4. Generation Architecture & Model

The blueprint generation follows a strict gatekeeper architecture:

```
Reviewed JD + Interview Config + Interview Policy
                      │
                      ▼
             LLM Semantic Planner
                      │
                      ▼
         Structured Candidate Blueprint
                      │
                      ▼
     Deterministic Validator / Normalizer
                      │
                      ▼
            Valid Saved Blueprint
```

### Architectural Rule:
> **LLM proposes. Domain code validates.**  
> Any candidate plan generated by the LLM is treated as untrusted data until it passes deterministic schema, budget, and policy validation.

---

## 5. Confirmed Generation Invariants (BR-01 to BR-13)

1. **Strict Lineage:** A Blueprint belongs to exactly one reviewed JD (`job_descriptions.id`).
2. **1:N Cardinality (JD to Blueprints):** One reviewed JD can produce multiple reusable Blueprints across different difficulty levels, durations, or focus areas.
3. **1:N Cardinality (Blueprint to Sessions):** One Blueprint can be executed across multiple independent runtime Sessions.
4. **Difficulty Independence:** Configured interview difficulty is independent of extracted JD seniority (e.g. mid-level JD can be practiced at senior difficulty).
5. **Question Budget Match:** The total stage question budgets in the Blueprint must exactly equal the configured `questionCount`.
6. **Time Allocation Boundedness:** Sum of stage `allocatedMinutes` must respect the configured interview duration and policy time bounds.
7. **Skill Traceability:** All evaluated skills and topics must trace directly to requirements in the Reviewed JD or explicit user-selected focus areas.
8. **WHAT vs. HOW Separation:** The Blueprint specifies assessment objectives, topics, and criteria; it must **NOT** contain final fixed question wording.
9. **Adaptive Runtime Questioning:** The runtime interview engine generates concrete questions and contextual follow-ups dynamically during turn-taking.
10. **Deterministic Validation Gate:** LLM candidate output is invalid and untrusted until deterministic domain validation passes.
11. **Immutable Session Snapshot:** When a session begins, a copy of the blueprint is frozen into `interview_sessions.blueprint_snapshot JSONB NOT NULL`. Subsequent changes or deletions to the Blueprint do not alter historical sessions.
12. **Non-Destructive Regeneration:** If regeneration of an existing Blueprint fails, the previously valid saved Blueprint remains untouched and available.
13. **Deletion Protection (`ON DELETE RESTRICT`):** Deleting a reusable Blueprint must **NOT** cascade-delete historical Sessions, turns, or performance reports.

---

## 6. Blueprint Domain Lifecycle

```
       [ Generation Requested ]
                  │
                  ▼
          ┌──────────────┐
          │  GENERATING  │◄─────────────┐
          └──────┬───────┘              │
                 │                      │
       ┌─────────┴─────────┐            │
Passes │                   │ Fails      │ Retry
       ▼                   ▼            │
┌──────────────┐   ┌──────────────┐     │
│    READY     │   │    FAILED    ├─────┘
└──────┬───────┘   └──────────────┘
       │ ▲
       │ │ Preview / Start Interview (Session A, B, C)
       └─┘ (reusable across sessions; does not consume blueprint)
```

### Lifecycle Semantics:
* **`GENERATING`:** Transient planning state while LLM creates candidate plan and domain validator executes checks.
* **`READY`:** Fully validated, persisted, reusable blueprint. Can be previewed repeatedly, reconfigured (triggering regeneration), or used to launch any number of independent sessions.
* **`FAILED`:** Recoverable error state when LLM generation or domain validation fails. Can be retried.
* *Note:* These lifecycle states represent domain logic semantics; they are not yet committed as a database enum.

---

## 7. Domain Failure Categories

When blueprint operations fail, domain errors fall into the following conceptual categories (HTTP status mappings deferred):

* **`InvalidReviewedJD`:** JD does not exist, is unreviewed (`is_reviewed = false`), or has no extracted requirements.
* **`InvalidInterviewConfiguration`:** Target duration, difficulty, or question count violates allowable policy ranges.
* **`BlueprintGenerationFailed`:** LLM adapter timeout, network partition, or unparseable upstream payload.
* **`InvalidGeneratedBlueprint`:** LLM candidate output failed deterministic domain validation (budget mismatch, unknown skills, invalid stage durations).
* **`BlueprintNotFound`:** Requested blueprint ID does not exist.
* **`BlueprintOwnershipViolation`:** Authenticated account does not own the requested Blueprint or its underlying JD.

---

## 8. Non-Goals

KAN-46 explicitly does **NOT** decide or finalize:
* Selection of LLM vendor or model (OpenAI, Gemini, Claude).
* Prompt wording or prompt template implementations.
* PDF extraction library selection (handled under [[KAN-44]]).
* REST endpoint route paths (e.g. `/api/v1/blueprints`).
* sqlc multi-package layout strategy (handled under [[KAN-19]]).
* STT/TTS engine selection (Whisper, Deepgram, ElevenLabs, Azure).
* 3D Avatar runtime rendering architecture.
* Exact algorithm for real-time adaptive questioning during turns.
* Final score calculation algorithm in performance reports.
* Canonical representation resolution between `parsed_data` and `job_description_skills`.

---

## 9. Architectural Artifacts

* **Target Database ERD:** [Target-Database-ERD.drawio](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.drawio) | [Target-Database-ERD.png](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.png) | [Target-Database-ERD.md](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/target-database/Target-Database-ERD.md)
* **Data Flow Diagram:** [jd-to-blueprint-dataflow.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-dataflow/jd-to-blueprint-dataflow.html) | [Dataflow JSON](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-dataflow/jd-to-blueprint-dataflow.json)
* **Sequence Diagram:** [generate-preview-save-execute-sequence.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-sequence/generate-preview-save-execute-sequence.html) | [Sequence JSON](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-sequence/generate-preview-save-execute-sequence.json)
* **Lifecycle Diagram:** [interview-blueprint-lifecycle.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-lifecycle/interview-blueprint-lifecycle.html) | [Lifecycle JSON](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-lifecycle/interview-blueprint-lifecycle.json)
* **Historical Baseline ERD:** [PR7-Database-ERD.drawio](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/pr7-database/PR7-Database-ERD.drawio)
