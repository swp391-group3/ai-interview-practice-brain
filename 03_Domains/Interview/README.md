---
project: SEP490
type: domain
status: draft
authority: reference
last_verified: 2026-09-11
---

# Real-Time Interview Simulation Domain

## 1. Subsystem Purpose
Coordinates the live interactive technical interview between candidate, AI interviewer, speech synthesis/recognition, and 3D avatar animation.

## 2. Core Components
- **Session Orchestrator:** Manages question selection from the [[JD-Blueprint]], follow-up generation, and conversation state machine.
- **WebSocket Gateway:** Low-latency bidirectional transport for audio streams and state updates.
- **Transcript Recorder:** Persists conversation turns for post-interview evaluation.

## 3. Reference Material
- See [[Interview-Contract]] for lifecycle states.
- See [[90_Legacy-Reference/Plans/IMPLEMENTATION_PLAN]] Section 2 for the proposed 13-state FSM.
