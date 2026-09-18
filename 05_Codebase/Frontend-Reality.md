---
project: SEP490
type: code-reality
status: current
authority: code
last_verified: 2026-09-18
---

# Frontend Implementation Reality

> **Ground Truth Audit:** Verified directly from `/home/dorriss/Projects/university/sep490/ai-interview-practice/frontend`

---

## 1. Concrete Code Facts (EXISTS IN CODE)

### Runtime & Core Libraries
- **Framework:** Next.js `16.3.4` (React `19.2.8`, App Router).
- **Package Manager:** Bun `1.4.0` (`bun.lock` present).
- **Styling:** Tailwind CSS `4.3.3`, `shadcn` `4.21.0`, Radix UI primitives.
- **Server State:** `@tanstack/react-query 5.102.8`.
- **Client State:** `zustand 5.0.15`.
- **Forms & Validation:** `react-hook-form 7.87.0`, `zod 4.5.4`, `@hookform/resolvers 5.9.1`.
- **3D Graphics Packages:** `three 0.185.1`, `@react-three/fiber 9.7.0`, `@react-three/drei 10.7.8`.
- **Testing:** `vitest 5.0.0`, `@playwright/test 1.63.0`.

### API Transport Architecture
- Custom typed fetch transport implemented in `frontend/src/lib/api/transport.ts` via `createApiTransport()`.
- **No Axios:** Axios is not installed in `package.json`.
- Enforces strict origin matching and relative paths.
- Decodes responses using supplied Zod or custom decoders.

### Design System Assets
- `frontend/design/DESIGN-CONTRACT.md`: Defines visual grammar and brand rules for "RoleCue".
- Brand assets: `rolecue-logo.svg`, `rolecue-icon.svg`, `rolecue-wordmark.svg`.
- Token specifications: `frontend/design/exploration/open-design-study/TOKENS.css`.

---

## 2. Feature Boundaries & Component State

| Feature Folder | Current Implementation Reality | Status |
| :--- | :--- | :--- |
| `features/job-description/` | Contains only `components/job-description-entry.tsx` displaying `RoutePlaceholder`. No forms or API mutations yet. | `PLACEHOLDER` (Subject to [[KAN-20]]) |
| `features/interview/` | Prototype folders for `avatar`, `audio`, `machine`, `transport`. | `SKELETON / SPIKE` |
| `features/auth/` | Session adapter skeleton (`session-adapter.ts`). | `IN PROGRESS` |
| `features/admin/` | Placeholder components. | `SKELETON` |
| `app/(candidate)/` | Route shells for `/profile`, `/reports`, `/settings`. | `SKELETON` |
