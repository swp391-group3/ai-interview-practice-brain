---
project: SEP490
type: contract
status: accepted
authority: code
last_verified: 2026-09-18
---

# Frontend Engineering Contract

## 1. Status & Metadata
- **Status:** `ACCEPTED` (Enforced by code in `frontend/`)
- **Framework:** Next.js 16.3 (App Router), React 19, TypeScript
- **Package Manager:** Bun (`bun@1.4.0`)
- **Styling:** Tailwind CSS v4, shadcn/ui
- **3D Graphics:** Three.js, `@react-three/fiber`, `@react-three/drei`
- **Testing:** Vitest, Playwright

## 2. Directory & Component Boundaries
```
frontend/src/
├── app/                           # Next.js route groups: (public), (candidate), admin
├── components/
│   ├── ui/                        # Low-level primitives (Button, Card, Input, Textarea)
│   ├── feedback/                  # State placeholders, toasts, loading spinners
│   └── layout/                    # Site shell, navigation bars, headers
├── config/                        # Routes, site metadata, permissions
├── features/                      # Domain features (job-description, interview, auth, admin)
├── lib/
│   └── api/                       # API client transport, error decoding, base configuration
└── providers/                     # React Query and app-level context providers
```

## 3. Engineering Invariants
- **API Transport:** All HTTP calls must use `createApiTransport` from `src/lib/api/transport.ts`. Axios is not used.
- **Server State Management:** Data fetching and mutations must use TanStack React Query v5.
- **Form State & Validation:** Forms must use React Hook Form with `@hookform/resolvers/zod` and co-located Zod schemas.
- **Feature Isolation:** Feature code in `features/<domain>` must encapsulate its own components, hooks, and domain queries.
- **Design Tokens:** Follow the RoleCue design system established in `frontend/design/DESIGN-CONTRACT.md`.

## 4. Open Questions
- WebGL avatar component lifecycle and canvas memory management during route transitions.

## 5. Traceability
- **Relevant Code:** `frontend/package.json`, `frontend/src/lib/api/transport.ts`, `frontend/design/DESIGN-CONTRACT.md`
- **Relevant Jira:** [[KAN-20]]
