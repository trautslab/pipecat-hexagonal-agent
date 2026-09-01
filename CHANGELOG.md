# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [1.4.0] - 2026-09-01

### Added
- **Integración Real con Google Calendar API v3 y OAuth2 (`GoogleCalendarClient`):** Conexión nativa con `https://www.googleapis.com/calendar/v3/calendars/primary/events` utilizando `GOOGLE_CALENDAR_CLIENT_ID` y `GOOGLE_CALENDAR_CLIENT_SECRET` de `.env`.
- **Ruta de Consentimiento y Callback (`GET /oauth2callback`):** Intercambio automático de códigos por `refresh_token` y `access_token` persistidos en `.agents/tokens/google_token.json`.
- **Botón de Autorización en 1 Clic en la UI (`[🔑 Autorizar Google Calendar]`):** Detección interactiva en el sidebar y en el chat para conectar la cuenta con Google Cloud.
- **Gobernanza AI-SDLC:** Caso de uso `UC-015`, diagrama `SEQ-013`, decisión `ADR-0014` y contrato `TASK-017`.

---

## [1.3.0] - 2026-09-01

### Added
- **Despacho Parametrizado de Herramientas MCP (`parse_calendar_parameters` & `create_calendar_event`):** Extracción inteligente de horas (`4:09`, `4:15`, etc.) y títulos (`Hello World`).
- **Barrera Anti-Rechazo (*Zero-Refusal Guard*):** Eliminación total de respuestas de rechazo (*"Lo siento, no puedo"*).
- **Gobernanza AI-SDLC:** Caso de uso `UC-014`, diagrama `SEQ-012`, decisión `ADR-0013` y contrato `TASK-016`.

---

## [1.2.0] - 2026-09-01

### Added
- **Rediseño Completo a Layout Postman / Modern IDE Workbench:** Estructura en 5 zonas visuales de alto rendimiento (Header, Sidebar, Workbench, Right Sidebar, Footer).
- **Gobernanza AI-SDLC:** Caso de uso `UC-013`, diagrama `SEQ-011`, decisión `ADR-0012` y contrato `TASK-015`.

---

## [1.1.0] - 2026-09-01

### Added
- **Persistencia en el Servidor Desacoplada del Navegador (`SessionRepositoryPort` & `FileSessionRepositoryAdapter`):** Almacenamiento agnóstico a clientes en `.agents/sessions/<session_id>.json`.
- **Endpoints REST de Sesiones (`/api/sessions`):** API para consulta (`GET`), persistencia (`POST`) y eliminación (`DELETE`) de conversaciones.
- **Gobernanza AI-SDLC:** Caso de uso `UC-012`, diagrama `SEQ-010`, decisión `ADR-0011` y contrato `TASK-014`.

---

## [1.0.0] - 2026-09-01

### Added
- **Motor Autónomo de Ejecución de MCPs (`MCPRuntimePort` & `MCPRuntimeAdapter`):** Ejecución 100% interna de subprocesos y herramientas MCP en segundo plano.
- **Prohibición Estricta de Directivas Pasivas:** Se eliminó cualquier sugerencia de comando manual al usuario (`npm run...`).
- **Gobernanza AI-SDLC:** Caso de uso `UC-011`, diagrama `SEQ-009`, decisión `ADR-0010` y contrato `TASK-013`.
