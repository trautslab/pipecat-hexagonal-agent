# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### Added
- Arquitectura Hexagonal con puertos `STTPort`, `LLMPort`, `TTSPort` y `TransportPort`.
- Core orquestador `VoiceAgentPipelineBuilder` con soporte para interrupciones (*barge-in*).
- Adaptadores locales 100% gratuitos para Faster-Whisper, Ollama, Piper/Kokoro TTS y Audio local.
- Adaptadores cloud listos para producción con Deepgram, OpenAI, Cartesia y Daily WebRTC.
- `AgentFactory` para inyección de dependencias declarativa vía `.env`.
- Entidad de dominio `AgentSession` para trazabilidad de contexto conversacional.
- Gobernanza AI-SDLC: `AGENTS.md`, `HANDOFF.md`, `CLAUDE.md`, diagramas C4, ADRs y Casos de Uso.
- Script de validación de invariantes arquitectónicos `scripts/validate_architecture.py`.
- Harness de evaluación automatizada `evals/harness.py`.
- Telemetría agéntica estructurada en `.agents/telemetry/events.jsonl`.
