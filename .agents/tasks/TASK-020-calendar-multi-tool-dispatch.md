# 📋 Contrato de Tarea: TASK-020 - Despachador Multi-Herramienta de Calendario y Listado de Eventos

- **ID de Tarea:** `TASK-020`
- **Caso de Uso:** [`UC-018`](../../docs/use-cases/UC-018-calendar-event-query-and-multi-action-tool-calling.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar `list_real_events` y `delete_real_event` en `GoogleCalendarClient` y `MCPRuntimeAdapter`, y configurar en `AutonomousReasoningEngine` la discriminación entre creación y consulta de eventos.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Usuario pregunta si el evento fue creado
  Given la solicitud "no veo lo que has configurado la verdad estás seguro que has hecho el recordatorio"
  When el clasificador de intenciones procesa el prompt
  Then detecta intención de consulta (list_events) y NO de creación
  And ejecuta google_calendar.list_real_events()
  And retorna la lista de eventos reales de Google Calendar sin crear eventos ficticios
```
