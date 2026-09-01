# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [1.6.0] - 2026-09-01

### Added
- **Razonamiento Nativo del LLM y Tool Calling Estructurado (`llm_reason_and_extract_tool_call`):** El propio modelo `llama3.1:8b` razona la intención del usuario, extrae los parámetros (título, fecha, hora, ubicación) y aplica reglas de proactividad y mejores prácticas directamente en un payload JSON antes de invocar las herramientas.
- **Redacción Proactiva de Recordatorios Amables por el LLM:** Generación de descripciones de calendario personalizadas con emojis, ubicaciones inferidas y buenos deseos.
- **Gobernanza AI-SDLC:** Caso de uso `UC-017`, diagrama `SEQ-015`, decisión `ADR-0016` y contrato `TASK-019`.

---

## [1.5.0] - 2026-09-01

### Added
- **Extractor Avanzado de Lenguaje Natural para Eventos (NLP Event Parser):** Extracción de títulos nombrados, fechas explícitas y horas con modificadores.
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
