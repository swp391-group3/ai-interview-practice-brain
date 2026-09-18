---
project: SEP490
type: control
status: current
authority: team
last_verified: 2026-09-18
---

# Open Architecture & Product Questions

## OQ-01: Blueprint contract versus implementation

**Status:** `REFINED — JIRA DONE; IMPLEMENTATION GAP REMAINS`. KAN-46 records the desired conceptual contract. Merged migration 000002 gives a separate `interview_blueprints` table and JD 1:N relationship, but does not re-parent sessions or prove all BR-01..BR-13. See [[JD-Blueprint]].

## OQ-02: Structured JD schema

**Status:** `RESOLVED — MERGED IMPLEMENTATION`. KAN-18 supplies the technical competency schema and deterministic validation. See [[JD-Extraction]].

## OQ-03: PDF library and ingestion strategy

**Status:** `OPEN`. KAN-44 is in progress; no verified local implementation decision.

## OQ-04: sqlc feature layout

**Status:** `RESOLVED — MERGED IMPLEMENTATION`. `api/sqlc.yaml` has separate auth and JD feature-repository entries.

## OQ-05: LLM provider/model policy

**Status:** `PARTIALLY RESOLVED`. Gemini/Eino is merged implementation reality. Long-term provider/model policy remains configurable/open; model is runtime configuration, not a permanent contract.

## Remaining unrelated questions

OQ-06 avatar/lip-sync is a spike; OQ-07 STT/TTS and OQ-08 payment gateway remain open. OQ-09 role enum versus product role vocabulary remains an open discrepancy.
