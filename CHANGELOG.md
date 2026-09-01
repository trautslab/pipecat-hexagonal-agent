# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [1.2.0] - 2026-09-01

### Added
- **Rediseño Completo a Layout Postman / Modern IDE Workbench:** Estructura en 5 zonas visuales de alto rendimiento:
  1. **Header:** Semáforo macOS (`🔴🟡🟢`), selector de workspace (`Aura Voice AI Workspace`), barra de búsqueda global (`⌘K`), selector de temas y estado de conexión.
  2. **Sidebar:** Árbol de navegación jerárquico con colecciones de conversaciones, herramientas MCP (Google Calendar, WebSearch) y secciones colapsables (`.env`, Specs, Persistencia).
  3. **Workbench:** Pestañas de sesión (`[🎙️ Sesión Activa •] [+]`), visualizador de audio Canvas con controles de voz superiores y panel de respuesta/timeline inferior con badges métricos (`200 OK • 144ms`).
  4. **Right Sidebar (Live Console & Copilot):** Consola ReAct en tiempo real con acordeones por turno, botón `[📋 Copiar Consola]` y entrada de prompt rápido por texto.
  5. **Footer:** Barra inferior con accesos a servidor, terminal y toggles para ocultar/mostrar paneles laterales.
- **Gobernanza AI-SDLC:** Caso de uso `UC-013`, diagrama `SEQ-011`, decisión `ADR-0012` y contrato `TASK-015`.

---

## [1.1.0] - 2026-09-01

### Added
- **Persistencia en el Servidor Desacoplada del Navegador (`SessionRepositoryPort` & `FileSessionRepositoryAdapter`):** Almacenamiento agnóstico a clientes en `.agents/sessions/<session_id>.json`.
- **Endpoints REST de Sesiones (`/api/sessions`):** API para consulta (`GET`), persistencia (`POST`) y eliminación (`DELETE`) de conversaciones y eventos de telemetría.
- **Gobernanza AI-SDLC:** Caso de uso `UC-012`, diagrama `SEQ-010`, decisión `ADR-0011` y contrato `TASK-014`.

---

## [1.0.0] - 2026-09-01

### Added
- **Motor Autónomo de Ejecución de MCPs (`MCPRuntimePort` & `MCPRuntimeAdapter`):** Ejecución 100% interna de subprocesos y herramientas MCP en segundo plano.
- **Prohibición Estricta de Directivas Pasivas:** Se eliminó cualquier sugerencia de comando manual al usuario (`npm run...`).
- **Gobernanza AI-SDLC:** Caso de uso `UC-011`, diagrama `SEQ-009`, decisión `ADR-0010` y contrato `TASK-013`.

---

## [0.9.0] - 2026-09-01

### Added
- **Ejecutor Activo de Herramientas MCP (`MCPExecutorPort` & `MCPExecutorAdapter`):** Validación de credenciales en `.env` y sonda de prueba de Google Calendar (*Hello World* en `now + 1 min`).
- **Gobernanza AI-SDLC:** Caso de uso `UC-010`, diagrama `SEQ-008`, decisión `ADR-0009` y contrato `TASK-012`.

---

## [0.8.0] - 2026-09-01

### Added
- **Consola Lateral Derecha de Trazabilidad en Tiempo Real (Right Sidebar):** Panel independiente para inspeccionar pensamientos, herramientas MCP, búsquedas y latencias.
- **Gobernanza AI-SDLC:** Caso de uso `UC-009`, diagrama `SEQ-007`, decisión `ADR-0008` y contrato `TASK-011`.
