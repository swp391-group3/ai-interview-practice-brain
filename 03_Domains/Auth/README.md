---
project: SEP490
type: domain
status: current
authority: code
last_verified: 2026-09-18
---

# Authentication & Identity Domain

**MERGED IMPLEMENTATION:** `api/internal/features/auth` provides account lookup, bcrypt password verification, and JWT pair generation. `POST /auth/login` is correctly mounted once; it returns the access token through the response envelope and writes the refresh JWT cookie (`refresh`, path `/auth/refresh`). Access and refresh secrets are separate configuration values.

`middleware.RequireAuth` accepts Bearer access tokens and places the authenticated UUID in Gin context; internal consumers use `middleware.CurrentUserID`.

The persisted role enum remains `participant`, `jury`, `admin`; its divergence from product terminology is deliberately retained as [[Open-Questions#OQ-09]].
