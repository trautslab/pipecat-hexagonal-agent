# 📋 Contrato de Tarea: TASK-021 - Enrutamiento Exhaustivo de Recordatorios y Aislamiento de Grounding

- **ID de Tarea:** `TASK-021`
- **Caso de Uso:** [`UC-019`](../../docs/use-cases/UC-019-reminder-synonym-routing-and-grounding-isolation.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
1. Corregir `GroundingService.should_search()` para eliminar la heurística `len(user_text.split()) >= 4` que enviaba recordatorios a búsqueda web.
2. Ampliar `AutonomousReasoningEngine.classify_calendar_intent()` para soportar `"hazme recordar"`, `"agendes"`, `"recuérdame"`, `"avísame"` y frases cotidianas de tareas domésticas y recordatorios.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Solicitud de recordatorio cotidiano para descongelar el pollo
  Given la solicitud "Hazme recordar para hoy a las 10 de la noche que tengo que descongelar el pollo"
  When el sistema procesa la solicitud
  Then GroundingService.should_search() retorna False
  And classify_calendar_intent() retorna 'create_event'
  And el evento se agenda en Google Calendar para las 22:00:00 con título "Descongelar el pollo"
```
