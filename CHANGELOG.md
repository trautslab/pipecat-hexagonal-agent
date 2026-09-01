# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [0.9.0] - 2026-09-01

### Added
- **Ejecutor Activo de Herramientas MCP (`MCPExecutorPort` & `MCPExecutorAdapter`):** Permite al agente validar credenciales en `.env` e invocar de manera real las herramientas de los servidores MCP sin solicitar configuraciones manuales o alucinar comandos.
- **Sonda Proactiva de Google Calendar (*Hello World*):** Al detectar credenciales configuradas, el agente agenda automáticamente un evento de prueba en Google Calendar programado para `now + 1 minuto`.
- **Gobernanza AI-SDLC:** Caso de uso `UC-010`, diagrama `SEQ-008`, decisión `ADR-0009` y contrato `TASK-012`.

---

## [0.8.0] - 2026-09-01

### Added
- **Consola Lateral Derecha de Trazabilidad en Tiempo Real (Right Sidebar):** Panel independiente a modo de consola de desarrollo para inspeccionar en tiempo real todos los pensamientos, llamadas a herramientas MCP, búsquedas web, latencias y modelos.
- **Streaming de Pasos en Vivo (`live_trace_step`):** Cada paso ReAct se transmite inmediatamente por WebSocket conforme ocurre en el backend, sin esperar a que el LLM termine su respuesta.
- **Numeración Correlativa por Turno (`#1`, `#2`, ...):** Identificadores correlativos en cada mensaje del chat y en los bloques desplegables de la consola derecha.
- **Botón `[📋 Copiar Consola]`:** Permite exportar de un solo clic toda la trazabilidad acumulada de la sesión en formato Markdown estructurado.
- **Gobernanza AI-SDLC:** Caso de uso `UC-009`, diagrama `SEQ-007`, decisión `ADR-0008` y contrato `TASK-011`.

---

## [0.7.0] - 2026-09-01

### Added
- **Inspector Desplegable de Acciones y Telemetría (`ActionInspector`):** Acordeón interactivo con el desglose cronológico de operaciones en cada respuesta.
- **Gobernanza AI-SDLC:** Caso de uso `UC-008`, diagrama `SEQ-006`, decisión `ADR-0007` y contrato `TASK-010`.

---

## [0.6.0] - 2026-09-01

### Added
- **Motor de Razonamiento Autónomo ReAct (Estilo OpenClaw / OpenHands):** Implementación de `AutonomousReasoningEngine` en `core/services/` para ejecutar bucles multi-paso (*Thought -> Action -> Observation -> Synthesis*).
- **Gestor Dinámico de Herramientas MCP (`MCPPort` & `MCPManagerAdapter`):** Permite al agente descubrir paquetes MCP en npm/GitHub, autoinstalar servidores en `.agents/mcp/mcp-servers.json` y declarar variables en `.env` (ej. Google Calendar MCP).
- **Gobernanza AI-SDLC:** Caso de uso `UC-007`, diagrama `SEQ-005`, decisión `ADR-0006` y contratos `TASK-008` / `TASK-009`.

---

## [0.5.0] - 2026-09-01

### Added
- **Sidebar de Historial de Conversaciones (ChatGPT / Claude UI):** Panel lateral retráctil con lista de chats guardados, botón `+ Nueva Conversación` y persistencia automática en `localStorage`.
- **Botón de Copiado Rápido (📋):** Icono de copiado en cada burbuja de mensaje con feedback interactivo (`✓ ¡Copiado!`).
- **Memoria Conversacional Multi-Turno:** El servidor mantiene el contexto de los mensajes de la sesión activa en Ollama.

---

## [0.4.0] - 2026-09-01

### Added
- **Herramienta de Búsqueda Web en Tiempo Real (`SearchPort` & `DuckDuckGoSearchAdapter`):** Permite al agente buscar información en internet a costo $0 sin requerir API keys.
- **Servicio de Grounding Anti-Alucinaciones (`GroundingService`):** Detecta preguntas factuales/geográficas y compone prompts enriquecidos con evidencias reales de internet antes de consultar al LLM.

---

## [0.3.0] - 2026-09-01

### Added
- **Selector de Temas Light & Dark Mode:** Soporte nativo para alternar entre temas claro y oscuro con persistencia en `localStorage`.
- **Servidor WebSocket RFC 6455 Nativo:** Implementación en `web_server.py` de handshake y framing de WebSocket binario/texto.

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
