---
project: SEP490
type: domain
status: current
authority: code
last_verified: 2026-09-11
---

# Authentication & Identity Domain

## 1. Status & Implementation Reality
- **Backend Package:** `api/internal/auth/` (fully implemented)
- **Database Table:** `accounts` (`api/migration/000001_init.up.sql`)
- **Key Modules:**
  - `repository/`: sqlc-generated account queries (`GetAccountByEmail`, `CreateAccount`).
  - `service/`: Password hashing (bcrypt) and token generation.
  - `transport/http/`: Gin HTTP handler for login (`api/internal/auth/transport/http/login.go`).
  - `pkg/token/`: Stateless JWT generation (access & refresh tokens).

## 2. Invariants & Security
- Passwords are encrypted with bcrypt.
- JWT tokens carry subject UUID, role, and token type (`access` vs `refresh`).
- Token validation middleware protects candidate and admin routes.

## 3. Discrepancies & Debt
- Route path bug: `api/internal/auth/transport/http/server.go` registers `/auth/auth/login`.
- Role ENUM in database has `participant`, `jury`, `admin`. Needs alignment with product specifications.
