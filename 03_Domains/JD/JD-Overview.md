---
project: SEP490
type: domain
status: current
authority: mixed
last_verified: 2026-09-18
---

# Job Description Domain Overview

```mermaid
flowchart LR
  Raw[Raw text / future PDF text] --> E[Extract technical competencies]
  E --> Review[Human review]
  Review --> Persist[Persist reviewed JD]
  Persist --> Blueprint[Blueprint assessment plan]
  Blueprint --> Session[Session execution]
```

**MERGED IMPLEMENTATION:** raw-text normalization, Eino/Gemini structured extraction, and deterministic validation (KAN-18).

**MERGED IMPLEMENTATION:** PR #15 separates Analyze from Create/List/Get/Update/Delete, persists reviewed caller-owned JDs, and introduces the database table for blueprints (KAN-19).

**JIRA / DESIRED STATE:** KAN-46 is Done; KAN-20, KAN-44 and KAN-45 are In Progress. PDF ingestion, review UI, dataset, and runtime interview realization must not be inferred from the merged extraction code.

See [[JD-Contract]] for canonical boundaries; diagrams in `architecture/` remain useful target/reference artifacts, not proof of full database implementation.
