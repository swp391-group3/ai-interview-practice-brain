---
project: SEP490
type: code-reality
status: current
authority: code
last_verified: 2026-09-18
---

# Monorepo Structure Map

```text
ai-interview-practice/
├── api/
│   ├── cmd/api/
│   ├── configs/
│   ├── internal/{config,database,handler,middleware,provider,router,server}/
│   ├── internal/features/{auth,jd}/
│   ├── internal/pkg/{ai,logger,tracer}/
│   ├── migration/
│   ├── pkg/{apperror,response,token}/
│   └── sqlc.yaml
├── frontend/                      # Next.js 16 application
└── docs/                          # source-repository documentation
```

`api/internal/features/jd` is merged for extraction. PR #15 additionally makes `features/jd/repository` and `handler/jd_handler.go` working code. Legacy paths `cmd/http`, `internal/auth`, `internal/shared`, and `pkg/util` are not current.
