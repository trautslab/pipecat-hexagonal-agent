# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [1.1.0] - 2026-09-01

### Added
- **Persistencia en el Servidor Desacoplada del Navegador (`SessionRepositoryPort` & `FileSessionRepositoryAdapter`):** Almacenamiento agnóstico a clientes en `.agents/sessions/<session_id>.json`. Permite cambiar de navegador (Chrome, Safari, Firefox) o migrar a una futura app móvil manteniendo el historial conversacional y la trazabilidad de la consola intactos.
- **Endpoints REST de Sesiones (`/api/sessions`):** API para consulta (`GET`), persistencia (`POST`) y eliminación (`DELETE`) de conversaciones y eventos de telemetría.
- **Persistencia en Tiempo Real de Pasos ReAct:** Cada pensamiento y acción emitido en la consola derecha se almacena automáticamente en el disco del backend.
- **Gobernanza AI-SDLC:** Caso de uso `UC-012`, diagrama `SEQ-010`, decisión `ADR-0011` y contrato `TASK-014`.

---

## [1.0.0] - 2026-09-01

### Added
- **Motor Autónomo de Ejecución de MCPs (`MCPRuntimePort` & `MCPRuntimeAdapter`):** Ejecución 100% interna de subprocesos y herramientas MCP en segundo plano.
- **Prohibición Estricta de Directivas Pasivas:** El System Prompt y el motor ReAct tienen estrictamente prohibido sugerir comandos manuales en la terminal al usuario (`npm run...`, etc.), ejecutando todas las acciones de forma autónoma.
- **Gobernanza AI-SDLC:** Caso de uso `UC-011`, diagrama `SEQ-009`, decisión `ADR-0010` y contrato `TASK-013`.

---

## [0.9.0] - 2026-09-01

### Added
- **Ejecutor Activo de Herramientas MCP (`MCPExecutorPort` & `MCPExecutorAdapter`):** Validación de credenciales en `.env` y sonda de prueba de Google Calendar (*Hello World* en `now + 1 min`).
- **Gobernanza AI-SDLC:** Caso de uso `UC-010`, diagrama `SEQ-008`, decisión `ADR-0009` y contrato `TASK-012`.

---

## [0.8.0] - 2026-09-01

### Added
- **Consola Lateral Derecha de Trazabilidad en Tiempo Real (Right Sidebar):** Panel independiente a modo de consola de desarrollo para inspeccionar en tiempo real todos los pensamientos, llamadas a herramientas MCP, búsquedas web, latencias y modelos.
- **Streaming de Pasos en Vivo (`live_trace_step`):** Cada paso ReAct se transmite inmediatamente por WebSocket conforme ocurre en el backend.
- **Numeración Correlativa por Turno (`#1`, `#2`, ...):** Identificadores correlativos en cada mensaje del chat y en la consola derecha.
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
- **Motor de Razonamiento Autónomo ReAct (Estilo OpenClaw / OpenHands):** Implementación de `AutonomousReasoningEngine` en `core/services/`.
- **Gestor Dinámico de Herramientas MCP (`MCPPort` & `MCPManagerAdapter`):** Autoinstalación de servidores en `.agents/mcp/mcp-servers.json` y `.env`.

---

## [0.5.0] - 2026-09-01

### Added
- **Sidebar de Historial de Conversaciones (ChatGPT / Claude UI):** Panel lateral retráctil con lista de chats guardados y botón `+ Nueva Conversación`.
- **Botón de Copiado Rápido (📋):** Icono de copiado en cada burbuja de mensaje con feedback interactivo.

---

## [0.4.0] - 2026-09-01

### Added
- **Herramienta de Búsqueda Web en Tiempo Real (`SearchPort` & `DuckDuckGoSearchAdapter`):** Costo $0 sin API keys.
- **Servicio de Grounding Anti-Alucinaciones (`GroundingService`):** Detección de preguntas factuales y composición de evidencias.

---

## [0.3.0] - 2026-09-01

### Added
- **Selector de Temas Light & Dark Mode:** Soporte nativo para alternar entre temas claro y oscuro con persistencia.
- **Servidor WebSocket RFC 6455 Nativo:** Framing de WebSocket binario/texto.

---

## [0.2.0] - 2026-09-01

### Added
- **Interfaz Web Interactiva (`web/`):** Cliente web con diseño Glassmorphism y visualizador de ondas.

---

## [0.1.0] - 2026-09-01

### Added
- Arquitectura Hexagonal con puertos `STTPort`, `LLMPort`, `TTSPort` y `TransportPort`.
- Pila local 100% gratuita para Faster-Whisper, Ollama y Piper TTS.
