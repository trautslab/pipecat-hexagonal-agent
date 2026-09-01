# 📋 Contrato de Tarea: TASK-012 - Ejecutor Activo de Herramientas MCP y Sonda de Google Calendar

- **ID de Tarea:** `TASK-012`
- **Caso de Uso:** [`UC-010`](../../docs/use-cases/UC-010-mcp-active-tool-execution.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar `MCPExecutorPort` y `MCPExecutorAdapter` para validar variables de `.env` y ejecutar activamente herramientas de servidores MCP (ej. agendamiento de prueba en Google Calendar para `now + 1 min`).

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Validación de credenciales y ejecución de prueba en Google Calendar
  Given un servidor "google-calendar" configurado en .agents/mcp/mcp-servers.json
  When el usuario indica que colocó las credenciales o pide probar el calendario
  Then MCPExecutorAdapter inspecciona .env
  And si las credenciales están presentes, programa un evento de prueba para dentro de 1 minuto
  And el motor ReAct emite la traza en vivo a la consola derecha
  And el agente responde confirmando la acción agendada
```
