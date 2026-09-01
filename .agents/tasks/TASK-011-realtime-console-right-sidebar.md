# 📋 Contrato de Tarea: TASK-011 - Consola Lateral Derecha de Trazabilidad en Tiempo Real

- **ID de Tarea:** `TASK-011`
- **Caso de Uso:** [`UC-009`](../../docs/use-cases/UC-009-realtime-telemetry-console-sidebar.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar en el servidor el streaming de eventos `live_trace` por WebSocket y en el cliente web el panel lateral derecho (Right Sidebar) con numeración correlativa y exportación Markdown de la consola.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Streaming de pasos en vivo en la consola lateral derecha
  Given una conversación activa con Aura
  When el usuario envía una consulta o solicita instalar un MCP
  Then se muestra inmediatamente el turno correlativo en la consola derecha
  And cada paso (análisis, acción, búsqueda) aparece en tiempo real con animación de pulso
  And en el chat principal el mensaje exhibe el número correlativo (#1, #2, ...)
  And el botón "[📋 Copiar Consola]" exporta la traza estructurada de todos los turnos al portapapeles
```
