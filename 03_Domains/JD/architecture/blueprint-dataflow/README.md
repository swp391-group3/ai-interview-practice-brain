# JD to Interview Blueprint Data Flow

> **Artifact:** `jd-to-blueprint-dataflow.html`  
> **Source Spec:** `jd-to-blueprint-dataflow.json`  
> **Archify Profile:** `showcase` (9/9 checks passed, 0 errors, 0 warnings)  
> **Type:** `dataflow`  

## Overview
Visualizes the end-to-end transformation of employer job postings into structured interview assessment plans:
1. **JD Ingestion:** Raw pasted JD text and PDF document parsing into clean UTF-8 text.
2. **Extraction & Review:** Structured entity parsing followed by candidate review and editing (**Reviewed JD** authority gate).
3. **Interview Inputs:** Reviewed JD combined with user-configured parameters (difficulty, duration, question budget) and platform interview policy.
4. **Blueprint Generation:** LLM Semantic Planner proposes candidate assessment objectives, followed by deterministic domain validation and normalization.
5. **Contract & Execution:** Persisted in `interview_blueprints` (**WHAT to assess**), snapshotted into `interview_sessions`, and delivered adaptively by the real-time engine (**HOW to ask**).

## Files
- Standalone HTML Viewer: [jd-to-blueprint-dataflow.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-dataflow/jd-to-blueprint-dataflow.html)
- Specification: [jd-to-blueprint-dataflow.json](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-dataflow/jd-to-blueprint-dataflow.json)
- Contact Sheet: [jd-to-blueprint-dataflow.visual-check.html](file:///home/dorriss/Documents/SEP490/03_Domains/JD/architecture/blueprint-dataflow/jd-to-blueprint-dataflow.visual-check.html)
