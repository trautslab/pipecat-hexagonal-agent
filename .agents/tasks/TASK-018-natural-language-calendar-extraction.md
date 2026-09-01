# 📋 Contrato de Tarea: TASK-018 - Extracción Avanzada de Eventos por Lenguaje Natural

- **ID de Tarea:** `TASK-018`
- **Caso de Uso:** [`UC-016`](../../docs/use-cases/UC-016-natural-language-event-extraction.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar en `AutonomousReasoningEngine` y `GoogleCalendarClient` la extracción de títulos personalizados, fechas completas (`1 de septiembre del 2026`), horas con modificadores (`5:15 de la tarde`), ubicación y descripciones amables.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Solicitud de evento con título nombrado y fecha explícita
  Given la solicitud "evento para las 5:15 de la tarde del 1 de septiembre del 2026 el evento llámalo preparación para ir al cine Planet de 2 de mayo"
  When el parser NLP procesa el prompt
  Then extrae title="Preparación para ir al cine Planet de 2 de mayo"
  And extrae date="2026-09-01" y time="17:15:00"
  And genera una descripción enriquecida con recordatorio amable
  And el evento se envía a Google Calendar API con dicho título y descripción
```
