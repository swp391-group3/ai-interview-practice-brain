# Interview Blueprint Lifecycle

> **Artifact:** `interview-blueprint-lifecycle.html`  
> **Source Spec:** `interview-blueprint-lifecycle.json`  
> **Archify Profile:** `showcase` (9/9 checks passed, 0 errors, 0 warnings)  
> **Type:** `lifecycle`  

## Overview
Models domain lifecycle states and invariants for Interview Blueprints:
* **`GENERATING`:** Active planning state while the LLM generates a candidate plan and domain validation runs.
* **`READY`:** Fully validated, persisted assessment plan. Reusable across multiple sessions (Session A, B, C). Can be previewed without mutation.
* **`FAILED`:** Error state when generation or validation fails. Retryable.

### Key Invariants:
* **Session Multiplicity:** One READY blueprint can launch multiple independent interview sessions. Starting a session does not consume the blueprint.
* **Non-Destructive Regeneration:** If a candidate attempts regeneration and it fails, the previous valid blueprint remains available.
* **Snapshot Immutability:** Historical sessions freeze `blueprint_snapshot` on creation.

## Files
- Standalone HTML Viewer: [interview-blueprint-lifecycle.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-lifecycle/interview-blueprint-lifecycle.html)
- Specification: [interview-blueprint-lifecycle.json](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-lifecycle/interview-blueprint-lifecycle.json)
- Contact Sheet: [interview-blueprint-lifecycle.visual-check.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-lifecycle/interview-blueprint-lifecycle.visual-check.html)
