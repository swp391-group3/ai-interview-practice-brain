---
project: SEP490
type: decision
status: accepted
authority: team
last_verified: 2026-09-11
---

# ADR-002: Database Access via pgx/v5 and sqlc Code Generation

## 1. Status
`ACCEPTED` (Implemented in `api/sqlc.yaml`, `api/pkg/util/database.go`, and `api/internal/auth/repository`)

## 2. Context & Problem Statement
The legacy specification proposed using GORM or plain ORM abstractions with Goose migrations. In Go production environments, ORMs frequently introduce runtime reflection overhead, opaque query generation, and complex debugging.

## 3. Decision Drivers
- High performance and full PostgreSQL feature support (JSONB, UUIDv4, custom ENUMs).
- Compile-time type safety for SQL queries without runtime reflection.
- Predictable and inspectable generated code.

## 4. Considered Options
- **Option A:** GORM (Active Record ORM).
- **Option B:** `sqlc` with `jackc/pgx/v5` connection pool.
- **Option C:** Pure raw `database/sql` with hand-written scanning.

## 5. Decision Outcome
Chosen option: **Option B (`sqlc` + `pgx/v5`)**.

### Migration Convention
- Schema migrations use `golang-migrate` formatted SQL files (`NNNNNN_name.up.sql`, `NNNNNN_name.down.sql`) stored in `api/migration/`.

### Consequences & Trade-offs
- **Positive:** SQL queries are written in pure `.sql` files. `sqlc` generates type-safe Go structs and query methods. Zero reflection cost.
- **Negative / Risks:** Developers must run `sqlc generate` after updating SQL queries or migrations.
