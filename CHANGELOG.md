# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [0.4.0] - 2026-09-01

### Added
- **Herramienta de Búsqueda Web en Tiempo Real (`SearchPort` & `DuckDuckGoSearchAdapter`):** Permite al agente buscar información en internet a costo $0 sin requerir API keys.
- **Servicio de Grounding Anti-Alucinaciones (`GroundingService`):** Detecta preguntas factuales/geográficas y compone prompts enriquecidos con evidencias reales de internet antes de consultar al LLM.
- **Integración en Servidor Web:** `web_server.py` ahora consulta evidencias de internet en vivo al recibir preguntas sobre ubicaciones, direcciones e instituciones.
- **Gobernanza AI-SDLC para Grounding:** Caso de uso `UC-005`, diagrama de secuencia `SEQ-003`, decisión `ADR-0004` y contrato `TASK-005`.
- **Harness de Evaluación:** Inclusión del benchmark para `TASK-005` en `evals/harness.py`.

---

## [0.3.0] - 2026-09-01

### Added
- **Selector de Temas Light & Dark Mode:** Soporte nativo para alternar entre temas claro y oscuro con persistencia en `localStorage` e iconografía fluida (☀️ / 🌙).
- **Servidor WebSocket RFC 6455 Nativo:** Implementación en `web_server.py` de handshake y framing de WebSocket binario/texto para conexión bidireccional inmediata.
- **Visualizador de Ondas Mejorado:** Renderizado reactivo en `<canvas>` con gradientes dinámicos adaptados al tema activo.

---

## [0.2.0] - 2026-09-01

### Added
- **Interfaz Web Interactiva (`web/`):** Cliente web en HTML/CSS/JS con diseño Glassmorphism, visualizador de ondas y subtítulos en streaming.
- **Adaptador de Transporte WebSocket (`WebSocketTransportAdapter`):** Permite la transmisión de tramas de audio PCM de baja latencia con el navegador.

---

## [0.1.0] - 2026-09-01

### Added
- Arquitectura Hexagonal con puertos `STTPort`, `LLMPort`, `TTSPort` y `TransportPort`.
- Core orquestador `VoiceAgentPipelineBuilder` con soporte para interrupciones (*barge-in*).
- Adaptadores locales 100% gratuitos para Faster-Whisper, Ollama, Piper/Kokoro TTS y Audio local.
- Adaptadores cloud con Deepgram, OpenAI, Cartesia y Daily WebRTC.
- Gobernanza AI-SDLC completa (`AGENTS.md`, `HANDOFF.md`, `CLAUDE.md`, diagramas C4, ADRs y Eval Harness).
