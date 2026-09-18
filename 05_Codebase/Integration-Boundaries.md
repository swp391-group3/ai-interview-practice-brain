---
project: SEP490
type: code-reality
status: current
authority: code
last_verified: 2026-09-18
---

# System Integration Boundaries

```mermaid
flowchart LR
  UI[Next.js frontend] --> T[createApiTransport / HTTP JSON]
  T --> R[Gin router; configurable port]
  R --> A[features/auth]
  R --> J[features/jd extraction — merged]
  A --> DB[(PostgreSQL)]
  J --> L[Gemini through Eino]
  J --> DB
  P[PR #15 only: /jds persistence + Swagger] -.-> R
```

Frontend does not access PostgreSQL, JWT secrets, or provider credentials. `response.Envelope` is the API transport boundary. The frontend fetch client must not assume null fields because envelope serialization uses `omitempty`.

`features/jd` extraction and external Gemini/Eino integration are merged. PR #15 persistence/API wiring is open; PDF, interview, speech, avatar, and payment integrations remain future or separate work.
