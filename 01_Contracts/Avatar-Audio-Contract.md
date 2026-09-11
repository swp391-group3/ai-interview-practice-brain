---
project: SEP490
type: contract
status: draft
authority: reference
last_verified: 2026-09-11
---

# Avatar & Audio Contract

## 1. Status & Metadata
- **Status:** `DRAFT` (Initial research spike in `@react-three/fiber`; production pipeline unfinalized)
- **Domain:** 3D WebGL Avatar Rendering, Viseme Lip-Sync, STT & TTS

## 2. Architecture & Components
1. **Candidate Audio Capture:** Browser Web Audio API / MediaRecorder with Voice Activity Detection (VAD).
2. **Speech-to-Text (STT):** Converts candidate speech to text with sub-500ms target latency.
3. **Text-to-Speech (TTS) + Viseme Generator:** Synthesizes audio speech along with phoneme/viseme timestamp arrays for avatar mouth blend-shapes.
4. **3D Avatar Presentation:** WebGL / Three.js canvas in Next.js frontend consuming viseme frames.

## 3. Degraded Mode Requirement
- If client device lacks WebGL2 support or drops below 20 FPS, system must support graceful degradation to a 2D animated waveform interface without interrupting the voice conversation.

## 4. Invariants
- Audio playback must strictly synchronize with 3D avatar facial morph targets.
- Avatar rendering thread must not block the network or audio streaming threads.

## 5. Open Questions
- Selection of STT/TTS providers (Whisper vs. Deepgram; Azure vs. ElevenLabs).
- Model format (Ready Player Me GLB vs. custom rigged 3D models).
- Rhubarb viseme processing: backend pre-computation vs. client-side estimation.

## 6. Traceability
- **Reference:** [[08_Reports/Lecturer/9_GFA26SE84_AI_Virtual_Technical_Interview_Capstone_Register.pdf]]
- **Code Pointers:** `frontend/src/features/interview/avatar`, `frontend/src/features/interview/audio`
