# 📋 Contrato de Tarea: TASK-008 - Motor de Razonamiento Autónomo ReAct

- **ID de Tarea:** `TASK-008`
- **Caso de Uso:** [`UC-007`](../../docs/use-cases/UC-007-openclaw-autonomous-reasoning-mcp.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar en `core/services/reasoning_engine.py` el bucle ReAct multi-paso capaz de alternar entre pensamientos (*thoughts*), invocaciones a herramientas (*actions*) y observaciones (*observations*) antes de emitir la síntesis final.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Bucle ReAct con autoinstalación de herramienta
  Given una solicitud del usuario para integrar un servicio externo (ej. Google Calendar)
  When el AutonomousReasoningEngine procesa la solicitud
  Then emite pensamientos estructurados
  And ejecuta la búsqueda web del MCP
  And ejecuta la autoinstalación con MCPManagerAdapter
  And sintetiza la respuesta final indicando las variables a configurar en .env
```
