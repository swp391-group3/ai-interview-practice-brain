---
project: SEP490
type: domain
status: current
authority: mixed
last_verified: 2026-09-18
---

# Interview Blueprint

## JIRA / DESIRED STATE — KAN-46 Done

The retained business contract separates JD requirements, reviewed JD, interview configuration, reusable blueprint, execution session, and historical snapshot. Its desired cardinality is JD 1:N Blueprint and Blueprint 1:N Session. A blueprint defines assessment objectives, timing, rubric and question budget; runtime questions remain adaptive rather than pre-baked.

## MERGED IMPLEMENTATION — PR #15

Migration 000002 drops `job_descriptions.blueprint`, then creates `interview_blueprints` with `id`, `job_description_id`, `difficulty`, `duration_minutes`, `question_count`, `blueprint_data`, `contract_version`, and timestamps. The JD foreign key is `ON DELETE RESTRICT`.

## GAP — do not silently normalize

The migration does **not** re-parent `interview_sessions` to `blueprint_id`, remove its redundant fields, create the full session lifecycle, or establish all BR-01..BR-13. Therefore the Target Database ERD, lifecycle, sequence, and data-flow artifacts are valuable proposed/reference design, not a complete implementation claim.

Links: [[JD-Contract]], [[KAN-46]], [Target ERD](architecture/target-database/Target-Database-ERD.md), [Lifecycle](architecture/blueprint-lifecycle/README.md).
