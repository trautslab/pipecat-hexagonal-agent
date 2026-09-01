# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [1.3.0] - 2026-09-01

### Added
- **Despacho Parametrizado de Herramientas MCP (`parse_calendar_parameters` & `create_calendar_event`):** Extracción inteligente de horas (`4:09` -> `04:09 p.m.` o `16:09:00`), títulos de eventos (`Hello World`) y referencias temporales directas desde el lenguaje natural del usuario.
- **Barrera Anti-Rechazo (*Zero-Refusal Guard*):** Eliminación total y blindaje contra respuestas de rechazo (*"Lo siento, no puedo cumplir con esa solicitud"*) o sugerencias de interacción manual, garantizando que el agente ejecute el 100% de las herramientas por su cuenta.
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
