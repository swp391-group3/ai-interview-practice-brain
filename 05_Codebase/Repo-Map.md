---
project: SEP490
type: code-reality
status: current
authority: code
last_verified: 2026-09-11
---

# Monorepo Structure Map

> **Repository:** `github.com/swp391-group3/ai-interview-practice`  
> **Local Path:** `/home/dorriss/Projects/university/sep490/ai-interview-practice`

---

## 1. Top-Level Directory Tree

```
ai-interview-practice/
├── .docker/                       # Docker & container compose configs
├── .env.example                   # Shared root environment template
├── api/                           # Go backend server
│   ├── cmd/http/main.go           # HTTP server entrypoint
│   ├── internal/                  # Private domain implementations
│   │   ├── auth/                  # Authentication domain (repository, service, transport)
│   │   └── shared/                # Server config, HTTP server builder
│   ├── migration/                 # Database migrations (000001_init.up.sql)
│   ├── pkg/                       # Public reusable packages
│   │   ├── apperror/              # AppError struct and domain error codes
│   │   ├── response/              # Unified JSON HTTP envelope
│   │   ├── token/                 # JWT token signing & claims
│   │   └── util/                  # PostgreSQL pool initialization
│   ├── go.mod                     # Go 1.27 dependencies
│   ├── go.sum
│   └── sqlc.yaml                  # sqlc query compilation settings
├── frontend/                      # Next.js 16 web application
│   ├── design/                    # RoleCue design system, brand assets, OpenDesign studies
│   ├── src/                       # Application source code
│   │   ├── app/                   # App Router pages ((candidate), admin, (public))
│   │   ├── components/            # UI components (shadcn/ui, layout, feedback)
│   │   ├── config/                # Route paths, permissions, site config
│   │   ├── features/              # Feature slices (job-description, interview, auth, admin)
│   │   ├── lib/api/               # Custom fetch transport & error handlers
│   │   └── providers/             # React Query & app providers
│   ├── package.json               # Next.js 16, React 19, Tailwind v4, Bun
│   └── bun.lock
└── docs/                          # Legacy documentation and capstone register markdown
```

---

## 2. Directory Separation Rules
- The backend root is `api/` (never `backend/`).
- The frontend root is `frontend/`.
- Cross-boundary communication occurs strictly over HTTP/REST and WebSockets via `frontend/src/lib/api/transport.ts`.
