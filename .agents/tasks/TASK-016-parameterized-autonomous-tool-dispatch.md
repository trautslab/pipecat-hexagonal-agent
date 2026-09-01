# 📋 Contrato de Tarea: TASK-016 - Despachador Parametrizado de Herramientas MCP y Barrera Anti-Rechazo

- **ID de Tarea:** `TASK-016`
- **Caso de Uso:** [`UC-014`](../../docs/use-cases/UC-014-zero-refusal-autonomous-tool-dispatch.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar extracción de parámetros de voz (horas, títulos), ejecutar `create_calendar_event` con parámetros reales en `MCPRuntimeAdapter` y habilitar la barrera anti-rechazo.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Solicitud con parámetros de hora y título
  Given un usuario que solicita "hacer una prueba de un Hello World para las 4:09"
  When el motor ReAct procesa el prompt
  Then extrae title="Hello World" y target_time="16:09:00"
  And ejecuta create_calendar_event con dichos parámetros
  And la respuesta final NO contiene "Lo siento, pero no puedo" ni directivas manuales
```
