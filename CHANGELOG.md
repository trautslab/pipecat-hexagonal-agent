# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [0.5.0] - 2026-09-01

### Added
- **Sidebar de Historial de Conversaciones (ChatGPT / Claude UI):** Panel lateral retráctil con lista de chats guardados, botón `+ Nueva Conversación` y persistencia automática en `localStorage`.
- **Botón de Copiado Rápido (📋):** Icono de copiado en cada burbuja de mensaje con feedback interactivo (`✓ ¡Copiado!`).
- **Autoconocimiento del Sistema & Scaffolding de MCPs:** Aura ahora asume el rol de ingeniera de software proactiva que comprende su arquitectura hexagonal y guía paso a paso la integración de servidores MCP (ej. Google Calendar), dejando al usuario únicamente la configuración de credenciales en `.env`.
- **Memoria Conversacional Multi-Turno:** El servidor `web_server.py` mantiene y alimenta el contexto completo de las sesiones activas a Ollama.
- **Gobernanza AI-SDLC:** Casos de uso `UC-006`, diagrama `SEQ-004`, decisión `ADR-0005`, y contratos `TASK-006` / `TASK-007`.

---

## [0.4.0] - 2026-09-01

### Added
- **Herramienta de Búsqueda Web en Tiempo Real (`SearchPort` & `DuckDuckGoSearchAdapter`):** Permite al agente buscar información en internet a costo $0 sin requerir API keys.
- **Servicio de Grounding Anti-Alucinaciones (`GroundingService`):** Detecta preguntas factuales/geográficas y compone prompts enriquecidos con evidencias reales de internet antes de consultar al LLM.

---

## [0.3.0] - 2026-09-01

### Added
- **Selector de Temas Light & Dark Mode:** Soporte nativo para alternar entre temas claro y oscuro con persistencia en `localStorage` e iconografía fluida (☀️ / 🌙).
- **Servidor WebSocket RFC 6455 Nativo:** Implementación en `web_server.py` de handshake y framing de WebSocket binario/texto para conexión bidireccional inmediata.

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
- Gobernanza AI-SDLC completa.
