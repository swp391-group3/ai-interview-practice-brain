---
project: SEP490
type: code-reality
status: current
authority: code
last_verified: 2026-09-11
---

# Backend Implementation Reality

> **Ground Truth Audit:** Verified directly from `/home/dorriss/Projects/university/sep490/ai-interview-practice/api`

---

## 1. Concrete Code Facts (EXISTS IN CODE)

### Language & Frameworks
- **Go Version:** `1.27.0` (specified in `api/go.mod`).
- **HTTP Routing:** `github.com/gin-gonic/gin v1.12.0`.
- **Database Driver:** `github.com/jackc/pgx/v5 v5.10.0` with `pgxpool`.
- **SQL Compiler:** `sqlc` v2 configured with `pgx/v5` engine.
- **Config Management:** `github.com/caarlos0/env/v11`.
- **Token Auth:** `github.com/golang-jwt/jwt/v5`.
- **Password Hashing:** `golang.org/x/crypto/bcrypt`.

### Implemented Packages & Files
| Package Path | Key Types / Functions | Verification Note |
| :--- | :--- | :--- |
| `cmd/http/main.go` | `main()`, `build()`, `gracefulShutdown()` | Listens on configured port, handles SIGINT/SIGTERM |
| `internal/shared/config/config.go` | `Config` struct | Parses `PORT`, `DATABASE_URL`, `CORS_ORIGIN`, `JWT_SECRET` |
| `internal/shared/transport/http/server.go` | `Build(cfg, pool)` | Initializes Gin engine, CORS middleware, mounts `/auth` routes |
| `internal/auth/repository/` | `account.sql.go`, `db.go`, `models.go` | `sqlc` generated methods for querying `accounts` table |
| `internal/auth/service/` | `AuthService`, `Login()`, `GenerateToken()` | Bcrypt password check, JWT token issuance |
| `internal/auth/transport/http/` | `Server`, `LoginRequest`, `Login()` | Validates request, handles `POST /auth/auth/login` |
| `pkg/apperror/apperr.go` | `AppError`, `Code` constants | `invalid_credentials`, `invalid_token`, `account_locked`, etc. |
| `pkg/response/response.go` | `Envelope`, `OK()`, `Created()`, `Error()` | Standard JSON response wrapper `{ success, data, error }` |
| `pkg/token/token.go` | `Sign()`, `Verify()`, `TokenPair` | Generates access token (15m) & refresh token (7d) |
| `pkg/util/database.go` | `NewDatabasePool(databaseURL)` | Configures `pgxpool.Pool` |
| `migration/000001_init.up.sql` | `accounts` table, `role` ENUM | Enum values: `participant`, `jury`, `admin` |

---

## 2. What DOES NOT Exist (PLANNED / REQUIRED)

> [!WARNING]
> None of the following exist in code. Do not assume or hallucinate their implementation:

- ❌ `api/internal/jd/`: **Does not exist.** (Active focus of [[KAN-18]], [[KAN-19]]).
- ❌ `api/internal/interview/`: **Does not exist.**
- ❌ `api/internal/avatar/` or audio processing: **Does not exist.**
- ❌ WebSocket server or interview FSM: **Does not exist.**
- ❌ LLM client integration (OpenAI/Gemini/Claude): **Does not exist.**
- ❌ PDF extraction pipeline: **Does not exist.** (Active focus of [[KAN-44]]).
- ❌ Redis client or caching layer: **Does not exist.** (Legacy spec artifact).
- ❌ GORM or Goose migrations: **Do not exist.** (Legacy spec artifact).
