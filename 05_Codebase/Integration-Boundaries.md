---
project: SEP490
type: code-reality
status: current
authority: local-brain
last_verified: 2026-09-11
---

# System Integration Boundaries

```mermaid
flowchart TB
    subgraph Client["Frontend Client (Next.js 16)"]
        UI["Candidate / Admin UI"]
        Transport["createApiTransport (Fetch)"]
        ThreeCanvas["Three.js / R3F Canvas"]
        AudioRec["Web Audio / VAD"]
    end

    subgraph Server["Backend Server (Go / Gin)"]
        Router["Gin HTTP Router (:8080)"]
        AuthModule["internal/auth"]
        JDModule["internal/jd (Planned)"]
        InterviewModule["internal/interview (Planned)"]
    end

    subgraph Storage["Data Tier (PostgreSQL 16)"]
        DB[(PostgreSQL Database)]
    end

    subgraph External["External Cloud Services"]
        LLM["LLM APIs (OpenAI / Gemini / Claude)"]
        STT_TTS["Speech Services (STT / TTS)"]
        PaymentGateway["Payment Gateway (VNPay / PayOS)"]
    end

    UI --> Transport
    Transport -- "HTTP/JSON (Envelope)" --> Router
    Router --> AuthModule
    Router --> JDModule
    Router --> InterviewModule
    AuthModule --> DB
    JDModule --> DB
    JDModule -.-> LLM
    InterviewModule -.-> LLM
    InterviewModule -.-> STT_TTS
    ThreeCanvas -.-> STT_TTS
```

## Boundary Rules
1. **Network Security:** Frontend never speaks directly to PostgreSQL or external payment secrets; all credentials pass through `api/`.
2. **Envelope Unpacking:** Frontend `createApiTransport` expects the `{ success, data, error }` response shape.
3. **Decoupled 3D Presentation:** WebGL canvas is driven purely by reactive props/state hooks; it does not handle HTTP requests directly.
