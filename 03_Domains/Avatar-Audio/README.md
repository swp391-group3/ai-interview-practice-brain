---
project: SEP490
type: domain
status: spike
authority: code
last_verified: 2026-09-11
---

# Virtual Avatar & Audio Domain

## 1. Scope & Capabilities
- **3D Avatar Rendering:** WebGL canvas using Three.js and `@react-three/fiber` / `@react-three/drei`.
- **Blend-Shape Lip-Sync:** Morph target animation driven by viseme timestamp data.
- **Voice Activity Detection (VAD):** Client-side speech boundary detection.
- **Speech Engines:** STT (Candidate voice -> text) and TTS (Interviewer text -> speech + visemes).

## 2. Current Implementation State
- Frontend repository has installed Three.js and R3F packages.
- Exploration components in `frontend/src/features/interview/avatar`.
- STT/TTS production providers remain `OPEN` (see [[Open-Questions]] OQ-06, OQ-07).
