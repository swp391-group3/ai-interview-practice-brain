---
project: SEP490
type: code-reality
status: current
authority: code
last_verified: 2026-09-18
---

# Monorepo Structure Map

## Related design source

`/home/dorriss/Projects/university/sep490/ai-interview-practice-design` is the standalone Design repository. Its `DESIGN-CONTRACT.md`, `brand/`, `product/SCREEN-INVENTORY.md`, and `product/FIGMA-PRODUCT-DESIGN-REPORT.md` are the canonical approved UI/UX source; `exploration/` is not automatically canonical. The Brain links cross-domain contracts rather than duplicating detailed design artifacts.

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

`api/internal/features/jd` is merged for extraction and persistence. PR #15 added `features/jd/repository` and `handler/jd_handler.go`, now merged. Legacy paths `cmd/http`, `internal/auth`, `internal/shared`, and `pkg/util` are not current.
