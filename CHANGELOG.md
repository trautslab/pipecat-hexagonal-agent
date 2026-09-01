# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [1.5.0] - 2026-09-01

### Added
- **Extractor Avanzado de Lenguaje Natural para Eventos (NLP Event Parser):**
  - Extracción precisa de títulos nombrados mediante cláusulas (`llámalo...`, `titulado...`, `con nombre...`).
  - Reconocimiento de fechas explícitas en español (`1 de septiembre del 2026` -> `2026-09-01`).
  - Detección de horas con modificadores (`5:15 de la tarde` -> `17:15:00`).
  - Detección automática de ubicaciones (`Cineplanet - 2 de Mayo`).
  - Generación de descripciones amables y estructuradas con emojis y recordatorios.
- **Gobernanza AI-SDLC:** Caso de uso `UC-016`, diagrama `SEQ-014`, decisión `ADR-0015` y contrato `TASK-018`.

---

## [1.4.0] - 2026-09-01

### Added
- **Integración Real con Google Calendar API v3 y OAuth2 (`GoogleCalendarClient`):** Conexión nativa con `https://www.googleapis.com/calendar/v3/calendars/primary/events` utilizando `GOOGLE_CALENDAR_CLIENT_ID` y `GOOGLE_CALENDAR_CLIENT_SECRET` de `.env`.
- **Ruta de Consentimiento y Callback (`GET /oauth2callback`):** Intercambio automático de códigos por `refresh_token` y `access_token` persistidos en `.agents/tokens/google_token.json`.
- **Gobernanza AI-SDLC:** Caso de uso `UC-015`, diagrama `SEQ-013`, decisión `ADR-0014` y contrato `TASK-017`.

---

## [1.3.0] - 2026-09-01

### Added
- **Despacho Parametrizado de Herramientas MCP (`parse_calendar_parameters` & `create_calendar_event`):** Extracción inteligente de horas y títulos.
- **Barrera Anti-Rechazo (*Zero-Refusal Guard*):** Eliminación total de respuestas de rechazo (*"Lo siento, no puedo"*).
- **Gobernanza AI-SDLC:** Caso de uso `UC-014`, diagrama `SEQ-012`, decisión `ADR-0013` y contrato `TASK-016`.

---

## [1.2.0] - 2026-09-01

### Added
- **Rediseño Completo a Layout Postman / Modern IDE Workbench:** Estructura en 5 zonas visuales de alto rendimiento (Header, Sidebar, Workbench, Right Sidebar, Footer).
- **Gobernanza AI-SDLC:** Caso de uso `UC-013`, diagrama `SEQ-011`, decisión `ADR-0012` y contrato `TASK-015`.
