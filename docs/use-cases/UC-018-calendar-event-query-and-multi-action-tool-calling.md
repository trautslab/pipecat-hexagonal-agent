# 🎯 Caso de Uso: UC-018 - Consulta y Despacho Multi-Herramienta de Calendario

- **ID:** `UC-018`
- **Dominio:** Multi-Action Tool Dispatch / Calendar Verification / Safe Execution
- **Actor Principal:** Usuario / LLM (Llama 3.1) / GoogleCalendarClient
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-016`](../diagrams/sequences/SEQ-016-calendar-query-and-multi-tool-dispatch.md)
- **Contrato de Tarea:** [`TASK-020`](../../.agents/tasks/TASK-020-calendar-multi-tool-dispatch.md)

---

## 📖 Descripción
El agente distingue cognitivamente entre órdenes de **creación**, **consulta/verificación** (`list_events`) y **eliminación** (`delete_event`), garantizando que ante preguntas de verificación o reclamo no se creen eventos falsos y se consulte el estado real del calendario en Google APIs.
