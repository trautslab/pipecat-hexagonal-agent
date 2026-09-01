# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [2.0.0] - 2026-09-01

### Changed (Major Architectural Transformation)
- **Arquitectura 100% LLM-First (Pure Cognitive Router):**
  - **Eliminación Total de Heurísticas en Python:** Suprimidas de forma definitiva todas las listas estáticas de palabras (`["hola", "buenos días", ...]`, `["crea", "agenda", ...]`), diccionarios de meses y regexes manuales en backend.
  - **Enrutador Cognitivo Unificado:** El modelo `llama3.1:8b` asume la responsabilidad completa de clasificar intenciones, seleccionar herramientas (`google_calendar.create_event`, `google_calendar.list_events`, `google_calendar.delete_event`, `mcp_manager.install_mcp`, `web_search`, `none`) y generar todos los parámetros enriquecidos (títulos limpios, fechas ISO, horas 24h y descripciones amables con emojis).
  - **Desacoplamiento Puro de Herramientas:** `GroundingService` ahora actúa como un ejecutor puro de búsqueda web cuando el LLM lo solicita explícitamente, evitando interferencias con recordatorios personales o tareas cotidianas.
- **Gobernanza AI-SDLC:** Caso de uso `UC-020`, diagrama `SEQ-018`, decisión `ADR-0019` y contrato `TASK-022`.

---

## [1.8.0] - 2026-09-01

### Added
- **Enrutamiento Exhaustivo de Recordatorios Cotidianos:** Reconocimiento de frases naturales y tareas domésticas.
- **Aislamiento Estricto de Búsqueda Web:** Eliminación de la regla `len >= 4` en Grounding.

---

## [1.7.0] - 2026-09-01

### Added
- **Despachador Multi-Herramienta de Calendario:** Discriminación entre creación, consulta/auditoría en vivo (`list_real_events`) y eliminación (`delete_real_event`).

---

## [1.6.0] - 2026-09-01

### Added
- **Razonamiento Nativo del LLM y Tool Calling Estructurado:** El propio modelo razona parámetros en JSON.
