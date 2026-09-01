# 🎯 Caso de Uso: UC-014 - Despacho Parametrizado de Herramientas MCP y Barrera Anti-Rechazo

- **ID:** `UC-014`
- **Dominio:** Autonomous Tool Calling / Semantic Parameter Extraction
- **Actor Principal:** Usuario / Agente de Software (Aura)
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-012`](../diagrams/sequences/SEQ-012-parameterized-mcp-tool-dispatch.md)
- **Contrato de Tarea:** [`TASK-016`](../../.agents/tasks/TASK-016-parameterized-autonomous-tool-dispatch.md)

---

## 📖 Descripción
El agente procesa solicitudes de voz o texto complejas que contienen parámetros dinámicos (ej. *"hacer una prueba de un Hello World para las 4:09"* o *"ya lo configuré, revísalo"*):
1. **Extracción Semántica:** Identifica horas específicas (ej. `4:09`), títulos de eventos (ej. `Hello World`) o cálculos relativos (`un minuto después`).
2. **Ejecución Inmediata:** Invoca `MCPRuntimeAdapter.create_calendar_event(title, time, date)` en segundo plano.
3. **Barrera Anti-Rechazo (*Zero-Refusal Guard*):** Prohíbe respuestas de rechazo (*"Lo siento, no puedo cumplir con esa solicitud"*) o sugerencias de hacerlo manualmente, entregando la confirmación de la acción ejecutada.
