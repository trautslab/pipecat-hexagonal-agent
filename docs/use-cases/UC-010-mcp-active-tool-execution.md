# 🎯 Caso de Uso: UC-010 - Ejecución Activa de Herramientas MCP y Prueba de Google Calendar

- **ID:** `UC-010`
- **Dominio:** MCP / Tool Execution / Automation
- **Actor Principal:** Usuario / Ingeniero de Software
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-008`](../diagrams/sequences/SEQ-008-mcp-live-tool-invocation.md)
- **Contrato de Tarea:** [`TASK-012`](../../.agents/tasks/TASK-012-mcp-active-executor.md)

---

## 📖 Descripción
Cuando el usuario indica que ya configuró las credenciales o solicita probar una herramienta MCP (como Google Calendar), el agente:
1. Inspecciona el archivo `.env` para verificar que las credenciales requeridas existan y no estén vacías.
2. Si están completas o en proceso de prueba, ejecuta activamente la herramienta MCP mediante `MCPExecutorAdapter`.
3. Para Google Calendar, crea un evento de prueba *"Hello World"* programado para un minuto en el futuro (`now + 1 min`) y retorna la confirmación del calendario.
4. Si falta alguna variable (ej. `GOOGLE_CALENDAR_CLIENT_SECRET`), indica específicamente qué clave falta completar en lugar de alucinar comandos inexistentes.
