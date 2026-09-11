# Generate, Preview, Save and Execute Interview Blueprint

> **Artifact:** `generate-preview-save-execute-sequence.html`  
> **Source Spec:** `generate-preview-save-execute-sequence.json`  
> **Archify Profile:** `showcase` (9/9 checks passed, 0 errors, 0 warnings)  
> **Type:** `sequence`  

## Overview
Depicts the complete sequence of interactions between the Candidate, Frontend, Blueprint Service, LLM Adapter, Domain Validator, Blueprint Repository, Session Service, and Interview Runtime:
1. **Configuration & JD Ingestion:** Candidate configures difficulty/duration; Frontend requests generation; Blueprint Service loads Reviewed JD.
2. **Planning & Domain Validation:** Blueprint Service invokes LLM Semantic Planner; candidate plan is evaluated by Domain Validator. Invalid plans are rejected without destroying previously valid blueprints.
3. **Persistence & Preview:** Valid blueprints are stored in `interview_blueprints` and previewed by the candidate. The plan is reusable.
4. **Session Start & Adaptive Turns:** Candidate starts an interview; Session Service copies an immutable `blueprint_snapshot`; Interview Runtime delivers dynamic questions and follow-ups based on turn context.

## Files
- Standalone HTML Viewer: [generate-preview-save-execute-sequence.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-sequence/generate-preview-save-execute-sequence.html)
- Specification: [generate-preview-save-execute-sequence.json](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-sequence/generate-preview-save-execute-sequence.json)
- Contact Sheet: [generate-preview-save-execute-sequence.visual-check.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-sequence/generate-preview-save-execute-sequence.visual-check.html)
