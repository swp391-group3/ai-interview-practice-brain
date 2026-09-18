---
project: SEP490
type: contract
status: current
authority: mixed
last_verified: 2026-09-18
---

# Job Description Contract

## Canonical concepts

- **JD:** raw description of job requirements.
- **Reviewed JD:** human-confirmed structured requirements.
- **Interview configuration:** practice parameters.
- **Blueprint:** reusable assessment plan, not a static question list.
- **Session:** one execution attempt; a session snapshot is the proposed historical-immutability mechanism.

## MERGED IMPLEMENTATION — extraction (KAN-18)

Extraction accepts normalized raw text and produces only validated technical competency data:

```json
{"title":"Backend Engineer","seniorityLevel":"senior","skills":[{"name":"Go","category":"programming_language","requirement":"required"}],"technologies":["Kafka"],"domainKnowledge":["Payments"]}
```

`title` and all three arrays are required; at least one nonblank competency across them is required. `seniorityLevel` is optional during extraction and is one of `intern`, `junior`, `mid`, `senior`, `lead`. Skill categories are `programming_language`, `framework`, `database`, `tool`, `technology`, `other`; requirement is `required`, `preferred`, or omitted. Soft skills are intentionally outside the current extraction contract.

Input must be valid UTF-8; line endings and whitespace are normalized; normalized length is 100–20,000 Unicode code points. Provider output is untrusted until deterministic validation succeeds. Case-insensitive duplicate names are deduplicated; conflicting duplicate skill metadata fails validation.

Gemini via Eino is **IMPLEMENTATION REALITY**. Provider and model are configured at runtime (`llm` configuration), so it is not a permanent product-vendor decision.

## OPEN PR / WORKING IMPLEMENTATION — reviewed persistence (KAN-19 / PR #15)

PR #15 persists caller-owned reviewed JDs through PostgreSQL/sqlc. `raw_text` is preserved; Create and Update validate reviewed fields, and reviewed persistence requires an explicitly selected seniority. Create stores status `customized`; Update changes structured fields, not raw text. Ownership-scoped queries make cross-user access behave as not-found.

The actual `job_descriptions` field concepts are `user_id`, `title`, `seniority_level`, `raw_text`, `parsed_data`, and `status`; old proposal-only names such as `account_id`, `is_reviewed`, and `raw_content` are superseded.

## Blueprint: contract versus database evidence

**JIRA / DESIRED STATE:** KAN-46 is Done and preserves the valuable BR-01..BR-13 business direction: JD 1:N blueprints, blueprint 1:N sessions, human review before use, runtime-adaptive questioning, and historical snapshots.

**OPEN PR / WORKING IMPLEMENTATION:** migration `000002_interview_blueprints.up.sql` drops `job_descriptions.blueprint` and creates `interview_blueprints(id, job_description_id, difficulty, duration_minutes, question_count, blueprint_data, contract_version, timestamps)`, with `job_description_id ... ON DELETE RESTRICT`.

**GAP:** that migration does not re-parent `interview_sessions` to `blueprint_id`, remove redundant session fields, or prove every BR-01..BR-13. The target ERD and diagrams remain proposed/reference design, not a statement of full implementation.

## Traceability

[[JD-Extraction]], [[JD-Persistence]], [[JD-Blueprint]], [[API-Contract]], [[KAN-18]], [[KAN-19]], [[KAN-46]].
