# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [0.2.0] - 2026-09-01

### Added
- **Interfaz Web Interactiva (`web/`):** Cliente web en HTML/CSS/JS con diseño Glassmorphism, Dark Mode, visualizador de ondas de audio en `<canvas>` en tiempo real y subtítulos en streaming.
- **Adaptador de Transporte WebSocket (`WebSocketTransportAdapter`):** Permite la transmisión bidireccional de tramas de audio PCM de baja latencia con el navegador.
- **Servidor Web Asíncrono (`web_server.py`):** Servidor HTTP y WebSocket ligero para servir el frontend y gestionar las conexiones de voz.
- **Gobernanza AI-SDLC para Web:** Caso de uso `UC-004`, diagrama de secuencia `SEQ-002`, decisión arquitectónica `ADR-0003` y contrato de tarea `TASK-004`.
- **Harness de Evaluación:** Inclusión del benchmark para `TASK-004` en `evals/harness.py`.

---

## [0.1.0] - 2026-09-01

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
