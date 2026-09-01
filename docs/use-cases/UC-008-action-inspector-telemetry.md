# 🎯 Caso de Uso: UC-008 - Inspector Desplegable de Acciones y Telemetría en la UI

- **ID:** `UC-008`
- **Dominio:** Observability / Telemetry / User Feedback
- **Actor Principal:** Usuario / Desarrollador
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-006`](../diagrams/sequences/SEQ-006-action-trace-inspector.md)
- **Contrato de Tarea:** [`TASK-010`](../../.agents/tasks/TASK-010-action-inspector-dropdown.md)

---

## 📖 Descripción
Cada respuesta generada por el asistente incluye un componente desplegable colapsable (`ActionInspector`) que contiene el registro completo y detallado de todas las acciones ejecutadas durante el turno conversacional:
- Pasos de pensamiento ReAct.
- Herramientas y llamadas a adaptadores (WebSearch, MCPManager).
- Archivos modificados o leídos (ej. `.agents/mcp/mcp-servers.json`, `.env`).
- Consultas enviadas y fragmentos devueltos.
- Marcas de tiempo y latencia total de ejecución.

El componente cuenta con un botón **`[📋 Copiar Registro]`** para exportar la traza estructurada al portapapeles y facilitar el feedback y la depuración del sistema.
