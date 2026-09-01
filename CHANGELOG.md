# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [1.8.0] - 2026-09-01

### Added
- **Enrutamiento Exhaustivo de Recordatorios Cotidianos (`classify_calendar_intent`):**
  - Reconocimiento de frases naturales como *"hazme recordar hoy a las 10 de la noche que tengo que descongelar el pollo"*, *"avísame"*, *"quiero que me agendes"*, *"recuérdame"*.
  - Extracción de títulos de tareas domésticas y recordatorios (*"Descongelar el pollo"*, *"Sacar del congelador el pollo"*).
- **Aislamiento Estricto de Búsqueda Web (`GroundingService`):**
  - Eliminada la regla genérica defectuosa `len(user_text.split()) >= 4` que enviaba recordatorios personales a DuckDuckGo Search.
  - La búsqueda web queda estrictamente limitada a preguntas factuales e investigación de internet.
- **Gobernanza AI-SDLC:** Caso de uso `UC-019`, diagrama `SEQ-017`, decisión `ADR-0018` y contrato `TASK-021`.

---

## [1.7.0] - 2026-09-01

### Added
- **Despachador Multi-Herramienta de Calendario (`classify_calendar_intent`):** Discriminación estricta entre creación, consulta/auditoría en vivo (`list_real_events`) y eliminación (`delete_real_event`).
- **Consulta en Tiempo Real de Google Calendar API v3 (`list_real_events`):** Auditoría directa contra la cuenta del usuario.
- **Gobernanza AI-SDLC:** Caso de uso `UC-018`, diagrama `SEQ-016`, decisión `ADR-0017` y contrato `TASK-020`.

---

## [1.6.0] - 2026-09-01

### Added
- **Razonamiento Nativo del LLM y Tool Calling Estructurado (`llm_reason_and_extract_tool_call`):** El propio modelo `llama3.1:8b` razona la intención del usuario y emite parámetros estructurados.
- **Gobernanza AI-SDLC:** Caso de uso `UC-017`, diagrama `SEQ-015`, decisión `ADR-0016` y contrato `TASK-019`.
