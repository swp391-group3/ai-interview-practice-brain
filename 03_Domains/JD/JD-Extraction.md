---
project: SEP490
type: domain
status: current
authority: code
last_verified: 2026-09-18
---

# JD Structured LLM Extraction

**Tracking:** [[KAN-18]] — `DONE` in Jira and **MERGED IMPLEMENTATION**.

`NormalizeInput` requires valid UTF-8, collapses whitespace per line, normalizes newline form, and accepts 100–20,000 Unicode code points. The Eino extractor sends the normalized JD as untrusted data to the configured Gemini-backed chat model. Its decoded response remains untrusted until `ValidateCandidate` completes.

```json
{"title":"Backend Engineer","seniorityLevel":null,"skills":[{"name":"Go","category":"programming_language"}],"technologies":[],"domainKnowledge":["Payments"]}
```

Title and all three arrays are structurally required; at least one nonblank competency is required. Seniority is optional when evidence is insufficient and may be `intern`, `junior`, `mid`, `senior`, or `lead`. Categories: `programming_language`, `framework`, `database`, `tool`, `technology`, `other`. Requirement can be `required`, `preferred`, or absent. The extraction prompt explicitly excludes interpersonal/soft skills.

Duplicate names are normalized case-insensitively; duplicate skills with conflicting category/requirement fail rather than silently choosing one. Validation uses `INVALID_JD_INPUT`, `JD_TOO_SHORT`, `JD_TOO_LONG`, and `INVALID_EXTRACTION_OUTPUT`; provider failures use `EXTRACTION_FAILED` where raised by the service.

Gemini/Eino is current implementation, while long-term provider/model policy is still [[Open-Questions#OQ-05]]. Stale fields such as `jobTitle`, `yearsOfExperience`, `domain`, `responsibilities`, `rawSummary`, `softSkills`, and `proficiency` are superseded.
