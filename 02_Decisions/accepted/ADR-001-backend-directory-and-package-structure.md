---
project: SEP490
type: decision
status: accepted
authority: team
last_verified: 2026-09-11
---

# ADR-001: Backend Directory and Feature-Based Modularization

## 1. Status
`ACCEPTED` (Implemented in repository root `api/` via PR #1)

## 2. Context & Problem Statement
Early speculative architecture documentation assumed a generic Clean Architecture / Hexagonal layer hierarchy under a `backend/` directory. This created excessive boilerplate (adapters, ports, inter-layer DTO conversions) for a graduation capstone team requiring high execution velocity.

## 3. Decision Drivers
- Developer ergonomics and high development speed.
- Co-location of domain business rules, HTTP handlers, and database queries.
- Clear separation between backend server (`api/`) and client application (`frontend/`).

## 4. Considered Options
- **Option A:** Strict Clean Architecture (`internal/domain`, `internal/usecase`, `internal/infrastructure`, `internal/interfaces`).
- **Option B:** Feature-based modular architecture (`api/internal/<domain>/{repository,service,transport}`).

## 5. Decision Outcome
Chosen option: **Option B (Feature-based modular architecture under `api/`)**.

### Package Layout
```
api/
├── cmd/http/main.go
├── internal/
│   ├── auth/
│   │   ├── repository/
│   │   ├── service/
│   │   └── transport/http/
│   ├── jd/ (planned)
│   └── shared/
│       ├── config/
│       └── transport/http/
├── migration/
└── pkg/
    ├── apperror/
    ├── response/
    ├── token/
    └── util/
```

### Consequences & Trade-offs
- **Positive:** Each feature domain (`auth`, `jd`, `interview`) is self-contained. Fast navigation and clear ownership.
- **Negative / Risks:** Must maintain cross-domain discipline to prevent circular package imports. Shared utilities live strictly in `pkg/` or `internal/shared/`.
